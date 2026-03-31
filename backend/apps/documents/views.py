import hashlib

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.audits.models import AuditEvent
from apps.documents.models import PolicyDocument
from apps.documents.serializers import (
    ControlStatementSerializer,
    DocumentSectionSerializer,
    PolicyDocumentSerializer,
)
from apps.documents.tasks import parse_and_extract_document
from apps.lineage.models import DocumentLineage


def checksum(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class PolicyDocumentViewSet(viewsets.ModelViewSet):
    queryset = PolicyDocument.objects.all().order_by("-effective_date", "-id")
    serializer_class = PolicyDocumentSerializer

    def create(self, request, *args, **kwargs):
        payload = request.data.copy()
        content_text = payload.get("content_text", "") or ""
        payload["sha256_checksum"] = checksum(content_text)

        existing = PolicyDocument.objects.filter(sha256_checksum=payload["sha256_checksum"]).first()
        if existing:
            serializer = self.get_serializer(existing)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)
        document = serializer.save()

        parse_and_extract_document.delay(document.id)

        AuditEvent.objects.create(
            entity_type="PolicyDocument",
            entity_id=str(document.id),
            event_type="document_created",
            actor_type=AuditEvent.ActorType.USER,
            correlation_id=getattr(request, "correlation_id", "document-create"),
            payload={"title": document.title, "version_label": document.version_label},
        )

        headers = self.get_success_headers(serializer.data)
        return Response(
            self.get_serializer(document).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @action(detail=True, methods=["get"])
    def sections(self, request, pk=None):
        document = self.get_object()
        serializer = DocumentSectionSerializer(document.sections.all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def statements(self, request, pk=None):
        document = self.get_object()
        serializer = ControlStatementSerializer(document.statements.all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def lineage(self, request, pk=None):
        document = self.get_object()
        links = DocumentLineage.objects.filter(
            parent_document=document
        ) | DocumentLineage.objects.filter(child_document=document)
        data = [
            {
                "id": link.id,
                "parent_document": link.parent_document_id,
                "child_document": link.child_document_id,
                "relationship_type": link.relationship_type,
            }
            for link in links
        ]
        return Response(data)
