import json
from pathlib import Path

from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.evals.models import EvalRun
from apps.evals.serializers import EvalRunSerializer


class EvalRunViewSet(ModelViewSet):
    queryset = EvalRun.objects.all().order_by("-created_at", "-id")
    serializer_class = EvalRunSerializer
    http_method_names = ["get", "post", "head", "options"]

    @action(detail=False, methods=["get"], url_path="reports/latest")
    def reports_latest(self, request):
        repo_root = Path(settings.BASE_DIR).parent
        latest_path = repo_root / "evals" / "reports" / "latest.json"
        if latest_path.exists():
            return Response(json.loads(latest_path.read_text(encoding="utf-8")))

        latest_run = EvalRun.objects.order_by("-created_at", "-id").first()
        if latest_run:
            return Response(latest_run.summary_metrics)
        return Response({})
