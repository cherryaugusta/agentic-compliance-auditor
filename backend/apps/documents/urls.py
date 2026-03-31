from rest_framework.routers import DefaultRouter

from .views import PolicyDocumentViewSet

router = DefaultRouter()
router.register("", PolicyDocumentViewSet, basename="documents")

urlpatterns = router.urls
