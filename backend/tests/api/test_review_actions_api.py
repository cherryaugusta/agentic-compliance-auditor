from datetime import date

import pytest
from apps.comparisons.models import ComparisonRun
from apps.documents.models import PolicyDocument
from apps.documents.tasks import parse_and_extract_document
from apps.findings.models import ConflictFlag
from apps.reviews.models import ReviewTask
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_review_task_assign_action_updates_task():
    reviewer = get_user_model().objects.create_user(
        username="reviewer1",
        email="reviewer1@example.com",
        password="Password123!",
    )

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

    source_document.refresh_from_db()
    target_document.refresh_from_db()

    source_statement = source_document.statements.first()
    target_statement = target_document.statements.first()

    assert source_statement is not None
    assert target_statement is not None

    run = ComparisonRun.objects.create(
        source_document=source_document,
        run_type=ComparisonRun.RunType.POLICY_VS_CONTROL,
        target_document_ids=[target_document.id],
        config_snapshot={},
        status=ComparisonRun.Status.COMPLETED,
        correlation_id="review-assign-test",
    )

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

    task = ReviewTask.objects.create(
        conflict_flag=finding,
        queue_name="policy-review",
        status=ReviewTask.Status.UNASSIGNED,
        reason_code=ReviewTask.ReasonCode.HIGH_SEVERITY,
        sla_due_at="2026-04-02T11:07:12Z",
    )

    client = APIClient()
    response = client.post(
        f"/api/review-tasks/{task.id}/assign/",
        {"username": reviewer.username},
        format="json",
    )

    task.refresh_from_db()

    assert response.status_code == 200
    assert task.status == ReviewTask.Status.ASSIGNED
    assert task.assigned_to is not None
    assert task.assigned_to.username == "reviewer1"


@pytest.mark.django_db
def test_review_task_approve_action_updates_task_and_conflict():
    reviewer = get_user_model().objects.create_user(
        username="reviewer1",
        email="reviewer1@example.com",
        password="Password123!",
    )

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

    source_document.refresh_from_db()
    target_document.refresh_from_db()

    source_statement = source_document.statements.first()
    target_statement = target_document.statements.first()

    assert source_statement is not None
    assert target_statement is not None

    run = ComparisonRun.objects.create(
        source_document=source_document,
        run_type=ComparisonRun.RunType.POLICY_VS_CONTROL,
        target_document_ids=[target_document.id],
        config_snapshot={},
        status=ComparisonRun.Status.COMPLETED,
        correlation_id="review-approve-test",
    )

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

    task = ReviewTask.objects.create(
        conflict_flag=finding,
        queue_name="policy-review",
        assigned_to=reviewer,
        status=ReviewTask.Status.ASSIGNED,
        reason_code=ReviewTask.ReasonCode.HIGH_SEVERITY,
        sla_due_at="2026-04-02T11:07:12Z",
    )

    client = APIClient()
    response = client.post(
        f"/api/review-tasks/{task.id}/approve/",
        {"comment": "Approved in test."},
        format="json",
    )

    task.refresh_from_db()
    finding.refresh_from_db()

    assert response.status_code == 200
    assert task.status == ReviewTask.Status.APPROVED
    assert finding.status == ConflictFlag.Status.CONFIRMED
