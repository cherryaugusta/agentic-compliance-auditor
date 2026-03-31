from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.findings.models import ConflictFlag
from apps.findings.serializers import (
    ConflictFlagSerializer,
    EvidenceCitationSerializer,
    FindingMemoSerializer,
)


class ConflictFlagViewSet(ReadOnlyModelViewSet):
    queryset = ConflictFlag.objects.all().order_by("-created_at", "-id")
    serializer_class = ConflictFlagSerializer

    @action(detail=True, methods=["get"])
    def citations(self, request, pk=None):
        finding = self.get_object()
        return Response(EvidenceCitationSerializer(finding.citations.all(), many=True).data)

    @action(detail=True, methods=["get"])
    def memo(self, request, pk=None):
        finding = self.get_object()
        if hasattr(finding, "memo"):
            return Response(FindingMemoSerializer(finding.memo).data)
        return Response(None)

    @action(detail=True, methods=["get"])
    def export_packet(self, request, pk=None):
        finding = self.get_object()
        return Response(
            {
                "id": finding.id,
                "conflict_type": finding.conflict_type,
                "severity": finding.severity,
                "status": finding.status,
                "reason_summary": finding.reason_summary,
                "rules_triggered": finding.rules_triggered,
                "citations": EvidenceCitationSerializer(finding.citations.all(), many=True).data,
                "memo": (
                    FindingMemoSerializer(finding.memo).data if hasattr(finding, "memo") else None
                ),
            }
        )
