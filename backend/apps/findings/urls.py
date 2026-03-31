from rest_framework.routers import DefaultRouter

from .views import ConflictFlagViewSet

router = DefaultRouter()
router.register("", ConflictFlagViewSet, basename="findings")

urlpatterns = router.urls
