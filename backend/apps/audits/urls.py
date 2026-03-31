from rest_framework.routers import DefaultRouter

from .views import AuditEventViewSet

router = DefaultRouter()
router.register("", AuditEventViewSet, basename="audit-events")

urlpatterns = router.urls
