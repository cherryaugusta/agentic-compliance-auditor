from rest_framework.routers import DefaultRouter

from .views import EvalRunViewSet

router = DefaultRouter()
router.register("runs", EvalRunViewSet, basename="eval-runs")

urlpatterns = router.urls
