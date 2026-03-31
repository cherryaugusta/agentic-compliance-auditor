import re
from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from apps.audits.models import AuditEvent
from apps.comparisons.models import ComparisonRun
from apps.documents.models import PolicyDocument
from apps.findings.models import ConflictFlag, EvidenceCitation, FindingMemo
from apps.observability.models import ModelExecutionLog, PromptVersion
from apps.reviews.models import ReviewTask
from apps.statements.models import ControlStatement


def extract_days(text: str) -> int | None:
    match = re.search(r"within\s+(\d+)\s+(business\s+days|days)", text, flags=re.IGNORECASE)
    return int(match.group(1)) if match else None


def extract_threshold(text: str) -> int | None:
    match = re.search(
        r"(?:above|over|greater than|more than)\s+(?:\u00A3)?([\d,]+)",
        text,
        flags=re.IGNORECASE,
    )
    return int(match.group(1).replace(",", "")) if match else None


def score_severity(conflict_type: str, source_value: int | None, target_value: int | None) -> str:
    if conflict_type in {
        ConflictFlag.ConflictType.TIMELINE_CONFLICT,
        ConflictFlag.ConflictType.THRESHOLD_CONFLICT,
    }:
        return ConflictFlag.Severity.HIGH
    if conflict_type == ConflictFlag.ConflictType.STALE_REFERENCE:
        return ConflictFlag.Severity.MEDIUM
    return ConflictFlag.Severity.MEDIUM


def active_prompt(purpose: str):
    return (
        PromptVersion.objects.filter(purpose=purpose, is_active=True)
        .order_by("-created_at")
        .first()
    )


def create_review_task(conflict: ConflictFlag, reason_code: str) -> ReviewTask:
    return ReviewTask.objects.create(
        conflict_flag=conflict,
        queue_name=getattr(settings, "DEFAULT_REVIEW_QUEUE", "policy-review"),
        status=ReviewTask.Status.UNASSIGNED,
        reason_code=reason_code,
        sla_due_at=timezone.now()
        + timedelta(hours=int(getattr(settings, "DEFAULT_SLA_HOURS", 48))),
    )


def compare_run(run: ComparisonRun) -> None:
    run.status = ComparisonRun.Status.RUNNING
    run.started_at = timezone.now()
    run.save(update_fields=["status", "started_at"])

    source_statements = list(run.source_document.statements.all())
    target_docs = list(PolicyDocument.objects.filter(id__in=run.target_document_ids))
    target_statements = list(ControlStatement.objects.filter(document__in=target_docs))

    contradiction_prompt = active_prompt(PromptVersion.Purpose.CONTRADICTION_ANALYSIS)
    degraded = contradiction_prompt is None

    for source in source_statements:
        for target in target_statements:
            if (
                source.statement_type == ControlStatement.StatementType.TIMELINE
                and target.statement_type == ControlStatement.StatementType.TIMELINE
            ):
                s = extract_days(source.raw_text)
                t = extract_days(target.raw_text)
                if s and t and s != t:
                    timeline_summary = (
                        f"Timeline mismatch: source={s} business days, "
                        f"target={t} business days."
                    )
                    conflict = ConflictFlag.objects.create(
                        comparison_run=run,
                        source_statement=source,
                        target_statement=target,
                        conflict_type=ConflictFlag.ConflictType.TIMELINE_CONFLICT,
                        severity=score_severity(
                            ConflictFlag.ConflictType.TIMELINE_CONFLICT,
                            s,
                            t,
                        ),
                        status=(
                            ConflictFlag.Status.NEEDS_REVIEW
                            if degraded
                            else ConflictFlag.Status.OPEN
                        ),
                        confidence=0.75 if degraded else 0.92,
                        requires_review=True,
                        reason_summary=timeline_summary,
                        rules_triggered=["timeline_mismatch"],
                        model_version=None if degraded else "mock-contradiction-model",
                    )
                    EvidenceCitation.objects.create(
                        conflict_flag=conflict,
                        document=source.document,
                        section=source.section,
                        citation_role=EvidenceCitation.CitationRole.SOURCE,
                        excerpt_text=source.raw_text,
                    )
                    EvidenceCitation.objects.create(
                        conflict_flag=conflict,
                        document=target.document,
                        section=target.section,
                        citation_role=EvidenceCitation.CitationRole.TARGET,
                        excerpt_text=target.raw_text,
                    )
                    FindingMemo.objects.create(
                        conflict_flag=conflict,
                        recommended_action=FindingMemo.RecommendedAction.REVIEW,
                        summary=conflict.reason_summary,
                        structured_rationale={
                            "source_statement": source.normalized_text,
                            "target_statement": target.normalized_text,
                            "degraded_mode": degraded,
                        },
                        confidence=conflict.confidence,
                        prompt_version=contradiction_prompt,
                    )
                    create_review_task(
                        conflict,
                        (
                            ReviewTask.ReasonCode.PROVIDER_FAILURE
                            if degraded
                            else ReviewTask.ReasonCode.HIGH_SEVERITY
                        ),
                    )

            if (
                source.statement_type == ControlStatement.StatementType.THRESHOLD
                and target.statement_type == ControlStatement.StatementType.THRESHOLD
            ):
                s = extract_threshold(source.raw_text)
                t = extract_threshold(target.raw_text)
                if s and t and s != t:
                    threshold_summary = f"Threshold mismatch: source={s}, target={t}."
                    conflict = ConflictFlag.objects.create(
                        comparison_run=run,
                        source_statement=source,
                        target_statement=target,
                        conflict_type=ConflictFlag.ConflictType.THRESHOLD_CONFLICT,
                        severity=score_severity(
                            ConflictFlag.ConflictType.THRESHOLD_CONFLICT,
                            s,
                            t,
                        ),
                        status=ConflictFlag.Status.OPEN,
                        confidence=0.9,
                        requires_review=True,
                        reason_summary=threshold_summary,
                        rules_triggered=["threshold_mismatch"],
                        model_version="mock-contradiction-model",
                    )
                    EvidenceCitation.objects.create(
                        conflict_flag=conflict,
                        document=source.document,
                        section=source.section,
                        citation_role=EvidenceCitation.CitationRole.SOURCE,
                        excerpt_text=source.raw_text,
                    )
                    EvidenceCitation.objects.create(
                        conflict_flag=conflict,
                        document=target.document,
                        section=target.section,
                        citation_role=EvidenceCitation.CitationRole.TARGET,
                        excerpt_text=target.raw_text,
                    )
                    FindingMemo.objects.create(
                        conflict_flag=conflict,
                        recommended_action=FindingMemo.RecommendedAction.REVIEW,
                        summary=conflict.reason_summary,
                        structured_rationale={"source_threshold": s, "target_threshold": t},
                        confidence=conflict.confidence,
                        prompt_version=contradiction_prompt,
                    )
                    create_review_task(conflict, ReviewTask.ReasonCode.HIGH_SEVERITY)

    if contradiction_prompt is None:
        ModelExecutionLog.objects.create(
            comparison_run=run,
            task_name="contradiction_analysis",
            provider_name="mock",
            model_name="disabled",
            prompt_version=None,
            latency_ms=0,
            status=ModelExecutionLog.Status.FALLBACK_USED,
            cost_estimate=0,
        )
        run.status = ComparisonRun.Status.DEGRADED
    else:
        ModelExecutionLog.objects.create(
            comparison_run=run,
            task_name="contradiction_analysis",
            provider_name="mock",
            model_name="mock-contradiction-model",
            prompt_version=contradiction_prompt,
            latency_ms=25,
            status=ModelExecutionLog.Status.SUCCESS,
            cost_estimate=0,
        )
        run.status = ComparisonRun.Status.COMPLETED

    run.finished_at = timezone.now()
    run.save(update_fields=["status", "finished_at"])

    AuditEvent.objects.create(
        entity_type="ComparisonRun",
        entity_id=str(run.id),
        event_type="comparison_completed",
        actor_type=AuditEvent.ActorType.JOB,
        correlation_id=run.correlation_id,
        payload={"status": run.status, "targets": run.target_document_ids},
    )
