from rest_framework.routers import DefaultRouter

from .views import ComparisonRunViewSet

router = DefaultRouter()
router.register("runs", ComparisonRunViewSet, basename="comparison-runs")

urlpatterns = router.urls
