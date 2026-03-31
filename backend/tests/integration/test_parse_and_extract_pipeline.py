from datetime import date

import pytest
from apps.documents.models import PolicyDocument
from apps.documents.tasks import parse_and_extract_document
from apps.statements.models import ControlStatement


@pytest.mark.django_db
def test_parse_and_extract_document_creates_section_and_statement():
    document = PolicyDocument.objects.create(
        document_type=PolicyDocument.DocumentType.INTERNAL_POLICY,
        title="Integration Test Policy",
        source_name="Test Source",
        domain_area=PolicyDocument.DomainArea.COMPLAINTS,
        owner_team="Compliance",
        version_label="v1",
        effective_date=date(2026, 1, 1),
        is_external_source=False,
        status=PolicyDocument.Status.ACTIVE,
        storage_path="demo_data/internal_policies/integration_test_policy.txt",
        sha256_checksum="",
        content_text="Escalated complaints must be acknowledged within 10 business days.",
    )

    parse_and_extract_document(document.id)

    document.refresh_from_db()

    assert document.sections.count() == 1
    assert document.statements.count() == 1

    section = document.sections.first()
    statement = document.statements.first()

    assert section is not None
    assert statement is not None
    assert section.text == "Escalated complaints must be acknowledged within 10 business days."
    assert statement.statement_type == ControlStatement.StatementType.TIMELINE
    assert statement.deadline_text == "within 10 business days"
    assert (
        statement.normalized_text
        == "escalated complaints must be acknowledged within 10 business days."
    )
