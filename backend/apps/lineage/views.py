from collections import defaultdict

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.lineage.models import DocumentLineage
from apps.lineage.serializers import DocumentLineageSerializer


class DocumentLineageViewSet(viewsets.ModelViewSet):
    queryset = DocumentLineage.objects.select_related("parent_document", "child_document").all()
    serializer_class = DocumentLineageSerializer

    @action(detail=False, methods=["get"], url_path="version-chains")
    def version_chains(self, request):
        grouped = defaultdict(list)
        for link in self.get_queryset():
            grouped[link.parent_document.title].append(
                {
                    "parent_document_id": link.parent_document_id,
                    "parent_title": link.parent_document.title,
                    "child_document_id": link.child_document_id,
                    "child_title": link.child_document.title,
                    "relationship_type": link.relationship_type,
                }
            )
        return Response(grouped)
