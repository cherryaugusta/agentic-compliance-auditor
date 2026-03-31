from django.contrib import admin

from apps.comparisons.models import ComparisonRun


@admin.register(ComparisonRun)
class ComparisonRunAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "source_document",
        "run_type",
        "status",
        "correlation_id",
        "started_at",
        "finished_at",
        "created_at",
    )
    list_filter = ("run_type", "status", "created_at", "started_at", "finished_at")
    search_fields = ("source_document__title", "correlation_id")
    ordering = ("-created_at", "-id")
