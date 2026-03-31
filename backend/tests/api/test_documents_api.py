from datetime import date

import pytest
from apps.documents.models import PolicyDocument
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_documents_list_returns_seeded_document_fields():
    document = PolicyDocument.objects.create(
        document_type=PolicyDocument.DocumentType.INTERNAL_POLICY,
        title="API Test Policy",
        source_name="Internal Policy Office",
        domain_area=PolicyDocument.DomainArea.COMPLAINTS,
        owner_team="Compliance",
        version_label="v1",
        effective_date=date(2026, 1, 15),
        is_external_source=False,
        status=PolicyDocument.Status.ACTIVE,
        storage_path="demo_data/internal_policies/api_test_policy.txt",
        sha256_checksum="checksum-1",
        content_text="Escalated complaints must be acknowledged within 10 business days.",
    )

    client = APIClient()
    response = client.get("/api/documents/")

    assert response.status_code == 200
    payload = response.json()

    assert payload["count"] == 1
    assert payload["results"][0]["id"] == document.id
    assert payload["results"][0]["title"] == "API Test Policy"


@pytest.mark.django_db
def test_documents_create_computes_checksum_and_returns_document():
    client = APIClient()
    payload = {
        "document_type": "internal_policy",
        "title": "Created API Policy",
        "source_name": "Internal Policy Office",
        "domain_area": "complaints",
        "owner_team": "Compliance",
        "version_label": "v1",
        "effective_date": "2026-01-15",
        "is_external_source": False,
        "status": "active",
        "storage_path": "demo_data/internal_policies/created_api_policy.txt",
        "content_text": "Escalated complaints must be acknowledged within 10 business days.",
    }

    response = client.post("/api/documents/", payload, format="json")

    assert response.status_code == 201
    body = response.json()

    assert body["title"] == "Created API Policy"
    assert body["sha256_checksum"]
    assert PolicyDocument.objects.count() == 1
