from datetime import date

import pytest
from apps.comparisons.models import ComparisonRun
from apps.documents.models import PolicyDocument
from apps.documents.tasks import parse_and_extract_document
from apps.findings.models import ConflictFlag, EvidenceCitation, FindingMemo
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_findings_list_returns_conflict():
    source_document = PolicyDocument.objects.create(
        document_type=PolicyDocument.DocumentType.INTERNAL_POLICY,
        title="Source Policy",
        source_name="Internal Policy Office",
        domain_area=PolicyDocument.DomainArea.COMPLAINTS,
        owner_team="Compliance",
        version_label="v1",
        effective_date=date(2026, 1, 15),
        is_external_source=False,
        status=PolicyDocument.Status.ACTIVE,
        storage_path="demo_data/internal_policies/source_policy.txt",
        sha256_checksum="source",
        content_text="Escalated complaints must be acknowledged within 10 business days.",
    )
    target_document = PolicyDocument.objects.create(
        document_type=PolicyDocument.DocumentType.CONTROL_LIBRARY,
        title="Target Control",
        source_name="Internal Standards Board",
        domain_area=PolicyDocument.DomainArea.COMPLAINTS,
        owner_team="Risk",
        version_label="v1",
        effective_date=date(2026, 2, 1),
        is_external_source=False,
        status=PolicyDocument.Status.ACTIVE,
        storage_path="demo_data/control_libraries/target_control.txt",
        sha256_checksum="target",
        content_text="Escalated complaints must be acknowledged within 5 business days.",
    )

    parse_and_extract_document(source_document.id)
    parse_and_extract_document(target_document.id)

    run = ComparisonRun.objects.create(
        source_document=source_document,
        run_type=ComparisonRun.RunType.POLICY_VS_CONTROL,
        target_document_ids=[target_document.id],
        config_snapshot={},
        status=ComparisonRun.Status.COMPLETED,
        correlation_id="findings-api-test",
    )
    finding = ConflictFlag.objects.create(
        comparison_run=run,
        source_statement=source_document.statements.first(),
        target_statement=target_document.statements.first(),
        conflict_type=ConflictFlag.ConflictType.TIMELINE_CONFLICT,
        severity=ConflictFlag.Severity.HIGH,
        status=ConflictFlag.Status.OPEN,
        confidence=0.92,
        requires_review=True,
        reason_summary="Timeline mismatch.",
        rules_triggered=["timeline_mismatch"],
        model_version="mock-contradiction-model",
    )

    client = APIClient()
    response = client.get("/api/findings/")

    assert response.status_code == 200
    payload = response.json()

    assert payload["count"] == 1
    assert payload["results"][0]["id"] == finding.id


@pytest.mark.django_db
def test_finding_export_packet_returns_citations_and_memo():
    source_document = PolicyDocument.objects.create(
        document_type=PolicyDocument.DocumentType.INTERNAL_POLICY,
        title="Source Policy",
        source_name="Internal Policy Office",
        domain_area=PolicyDocument.DomainArea.COMPLAINTS,
        owner_team="Compliance",
        version_label="v1",
        effective_date=date(2026, 1, 15),
        is_external_source=False,
        status=PolicyDocument.Status.ACTIVE,
        storage_path="demo_data/internal_policies/source_policy.txt",
        sha256_checksum="source",
        content_text="Escalated complaints must be acknowledged within 10 business days.",
    )
    target_document = PolicyDocument.objects.create(
        document_type=PolicyDocument.DocumentType.CONTROL_LIBRARY,
        title="Target Control",
        source_name="Internal Standards Board",
        domain_area=PolicyDocument.DomainArea.COMPLAINTS,
        owner_team="Risk",
        version_label="v1",
        effective_date=date(2026, 2, 1),
        is_external_source=False,
        status=PolicyDocument.Status.ACTIVE,
        storage_path="demo_data/control_libraries/target_control.txt",
        sha256_checksum="target",
        content_text="Escalated complaints must be acknowledged within 5 business days.",
    )

    parse_and_extract_document(source_document.id)
    parse_and_extract_document(target_document.id)

    run = ComparisonRun.objects.create(
        source_document=source_document,
        run_type=ComparisonRun.RunType.POLICY_VS_CONTROL,
        target_document_ids=[target_document.id],
        config_snapshot={},
        status=ComparisonRun.Status.COMPLETED,
        correlation_id="findings-export-test",
    )

    source_statement = source_document.statements.first()
    target_statement = target_document.statements.first()

    assert source_statement is not None
    assert target_statement is not None

    finding = ConflictFlag.objects.create(
        comparison_run=run,
        source_statement=source_statement,
        target_statement=target_statement,
        conflict_type=ConflictFlag.ConflictType.TIMELINE_CONFLICT,
        severity=ConflictFlag.Severity.HIGH,
        status=ConflictFlag.Status.OPEN,
        confidence=0.92,
        requires_review=True,
        reason_summary="Timeline mismatch.",
        rules_triggered=["timeline_mismatch"],
        model_version="mock-contradiction-model",
    )

    EvidenceCitation.objects.create(
        conflict_flag=finding,
        document=source_document,
        section=source_statement.section,
        citation_role=EvidenceCitation.CitationRole.SOURCE,
        excerpt_text="Source excerpt",
    )
    EvidenceCitation.objects.create(
        conflict_flag=finding,
        document=target_document,
        section=target_statement.section,
        citation_role=EvidenceCitation.CitationRole.TARGET,
        excerpt_text="Target excerpt",
    )
    FindingMemo.objects.create(
        conflict_flag=finding,
        recommended_action=FindingMemo.RecommendedAction.REVIEW,
        summary="Review this finding.",
        structured_rationale={"reason": "timeline"},
        confidence=0.92,
    )

    client = APIClient()
    response = client.get(f"/api/findings/{finding.id}/export_packet/")

    assert response.status_code == 200
    payload = response.json()

    assert payload["id"] == finding.id
    assert payload["conflict_type"] == "timeline_conflict"
    assert len(payload["citations"]) == 2
    assert payload["memo"]["summary"] == "Review this finding."
