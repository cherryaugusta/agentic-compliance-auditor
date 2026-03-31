from rest_framework.routers import DefaultRouter

from .views import DocumentLineageViewSet

router = DefaultRouter()
router.register("", DocumentLineageViewSet, basename="lineage")

urlpatterns = router.urls
