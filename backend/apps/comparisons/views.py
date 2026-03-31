import uuid

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.comparisons.models import ComparisonRun
from apps.comparisons.serializers import ComparisonRunSerializer
from apps.comparisons.tasks import run_comparison


class ComparisonRunViewSet(viewsets.ModelViewSet):
    queryset = ComparisonRun.objects.all().order_by("-created_at", "-id")
    serializer_class = ComparisonRunSerializer

    def perform_create(self, serializer):
        run = serializer.save(correlation_id=str(uuid.uuid4()))
        run_comparison.delay(run.id)

    @action(detail=True, methods=["post"])
    def retry(self, request, pk=None):
        original = self.get_object()
        replay = ComparisonRun.objects.create(
            source_document=original.source_document,
            run_type=original.run_type,
            target_document_ids=original.target_document_ids,
            config_snapshot=original.config_snapshot,
            status=ComparisonRun.Status.PENDING,
            correlation_id=str(uuid.uuid4()),
        )
        run_comparison.delay(replay.id)
        return Response(self.get_serializer(replay).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def replay(self, request, pk=None):
        original = self.get_object()
        replay = ComparisonRun.objects.create(
            source_document=original.source_document,
            run_type=original.run_type,
            target_document_ids=original.target_document_ids,
            config_snapshot=original.config_snapshot,
            status=ComparisonRun.Status.PENDING,
            correlation_id=str(uuid.uuid4()),
        )
        run_comparison.delay(replay.id)
        return Response(self.get_serializer(replay).data, status=status.HTTP_201_CREATED)
