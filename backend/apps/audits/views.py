from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.audits.models import AuditEvent
from apps.audits.serializers import AuditEventSerializer


class AuditEventViewSet(ReadOnlyModelViewSet):
    queryset = AuditEvent.objects.all().order_by("-created_at", "-id")
    serializer_class = AuditEventSerializer
