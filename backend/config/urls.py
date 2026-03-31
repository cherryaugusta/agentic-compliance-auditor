from apps.observability.views import MetricsConflictsView, MetricsOverviewView, MetricsReviewOpsView
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("health/", include("apps.health.urls")),
    path("api/documents/", include("apps.documents.urls")),
    path("api/lineage/", include("apps.lineage.urls")),
    path("api/comparisons/", include("apps.comparisons.urls")),
    path("api/findings/", include("apps.findings.urls")),
    path("api/review-tasks/", include("apps.reviews.urls")),
    path("api/audit-events/", include("apps.audits.urls")),
    path("api/evals/", include("apps.evals.urls")),
    path("api/metrics/overview/", MetricsOverviewView.as_view()),
    path("api/metrics/review-ops/", MetricsReviewOpsView.as_view()),
    path("api/metrics/conflicts/", MetricsConflictsView.as_view()),
]
