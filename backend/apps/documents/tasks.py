import hashlib
import re

from celery import shared_task

from apps.audits.models import AuditEvent
from apps.documents.models import DocumentSection, PolicyDocument
from apps.statements.models import ControlStatement

TIMELINE_RE = re.compile(r"within\s+(\d+)\s+(business\s+days|days)", re.IGNORECASE)
THRESHOLD_RE = re.compile(
    r"(above|over|greater than|more than)\s+(?:\u00A3)?(\d[\d,]*)",
    re.IGNORECASE,
)


def _split_sections(text: str) -> list[str]:
    parts = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
    return parts or [text.strip()]


def _normalize(text: str) -> str:
    return " ".join(text.lower().split())


def _statement_type(text: str) -> str:
    if TIMELINE_RE.search(text):
        return ControlStatement.StatementType.TIMELINE
    if THRESHOLD_RE.search(text):
        return ControlStatement.StatementType.THRESHOLD
    if "approve" in text.lower():
        return ControlStatement.StatementType.APPROVAL_RULE
    if "must" in text.lower() or "required" in text.lower():
        return ControlStatement.StatementType.OBLIGATION
    return ControlStatement.StatementType.CONTROL


def _checksum(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@shared_task
def parse_and_extract_document(document_id: int) -> None:
    document = PolicyDocument.objects.get(id=document_id)
    if not document.sha256_checksum:
        document.sha256_checksum = _checksum(document.content_text)
        document.save(update_fields=["sha256_checksum"])

    document.sections.all().delete()
    document.statements.all().delete()

    for index, chunk in enumerate(_split_sections(document.content_text), start=1):
        section = DocumentSection.objects.create(
            document=document,
            section_index=index,
            heading=f"Section {index}",
            text=chunk,
            char_start=0,
            char_end=len(chunk),
            parser_confidence=0.99,
        )
        ControlStatement.objects.create(
            document=document,
            section=section,
            statement_type=_statement_type(chunk),
            raw_text=chunk,
            normalized_text=_normalize(chunk),
            deadline_text=TIMELINE_RE.search(chunk).group(0) if TIMELINE_RE.search(chunk) else None,
            threshold_text=(
                THRESHOLD_RE.search(chunk).group(0) if THRESHOLD_RE.search(chunk) else None
            ),
            schema_valid=True,
            extraction_confidence=0.95,
            extraction_version="v1",
        )

    AuditEvent.objects.create(
        entity_type="PolicyDocument",
        entity_id=str(document.id),
        event_type="parse_and_extract_completed",
        actor_type=AuditEvent.ActorType.JOB,
        correlation_id="parse-and-extract",
        payload={"document_title": document.title},
    )
