from rest_framework.routers import DefaultRouter

from .views import ReviewTaskViewSet

router = DefaultRouter()
router.register("", ReviewTaskViewSet, basename="review-tasks")

urlpatterns = router.urls
