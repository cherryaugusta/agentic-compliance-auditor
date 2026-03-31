from datetime import date

import pytest
from apps.comparisons.models import ComparisonRun
from apps.comparisons.tasks import run_comparison
from apps.documents.models import PolicyDocument
from apps.documents.tasks import parse_and_extract_document
from apps.findings.models import ConflictFlag, EvidenceCitation, FindingMemo
from apps.observability.models import ModelExecutionLog, PromptVersion
from apps.reviews.models import ReviewTask


@pytest.mark.django_db
def test_comparison_run_creates_conflict_citations_memo_and_review_task():
    PromptVersion.objects.create(
        name="contradiction-analysis-default",
        version_label="v1",
        purpose=PromptVersion.Purpose.CONTRADICTION_ANALYSIS,
        template_text="Draft contradiction rationale.",
        schema_version="v1",
        is_active=True,
    )

    source = PolicyDocument.objects.create(
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

    target = PolicyDocument.objects.create(
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

    parse_and_extract_document(source.id)
    parse_and_extract_document(target.id)

    run = ComparisonRun.objects.create(
        source_document=source,
        run_type=ComparisonRun.RunType.POLICY_VS_CONTROL,
        target_document_ids=[target.id],
        config_snapshot={"seeded": False},
        status=ComparisonRun.Status.PENDING,
        correlation_id="test-correlation-id",
    )

    run_comparison(run.id)

    run.refresh_from_db()

    assert run.status == ComparisonRun.Status.COMPLETED
    assert ConflictFlag.objects.count() == 1
    assert EvidenceCitation.objects.count() == 2
    assert FindingMemo.objects.count() == 1
    assert ReviewTask.objects.count() == 1
    assert ModelExecutionLog.objects.count() == 1

    finding = ConflictFlag.objects.get()

    assert finding.conflict_type == ConflictFlag.ConflictType.TIMELINE_CONFLICT
    assert finding.severity == ConflictFlag.Severity.HIGH
    assert (
        finding.reason_summary
        == "Timeline mismatch: source=10 business days, target=5 business days."
    )
    assert finding.rules_triggered == ["timeline_mismatch"]

    review_task = ReviewTask.objects.get()

    assert review_task.conflict_flag_id == finding.id
    assert review_task.status == ReviewTask.Status.UNASSIGNED
