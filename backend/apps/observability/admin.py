from django.contrib import admin

from apps.observability.models import GuidanceSource, ModelExecutionLog, PromptVersion


@admin.register(GuidanceSource)
class GuidanceSourceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "document",
        "source_type",
        "reference_code",
        "effective_date",
        "active",
        "created_at",
    )
    list_filter = ("source_type", "active", "effective_date", "created_at")
    search_fields = ("document__title", "reference_code")
    ordering = ("-effective_date", "-id")


@admin.register(PromptVersion)
class PromptVersionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "version_label",
        "purpose",
        "schema_version",
        "is_active",
        "created_at",
    )
    list_filter = ("purpose", "is_active", "schema_version", "created_at")
    search_fields = ("name", "version_label", "template_text")
    ordering = ("-created_at", "-id")


@admin.register(ModelExecutionLog)
class ModelExecutionLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "comparison_run",
        "task_name",
        "provider_name",
        "model_name",
        "status",
        "latency_ms",
        "created_at",
    )
    list_filter = ("status", "provider_name", "model_name", "task_name", "created_at")
    search_fields = ("task_name", "provider_name", "model_name")
    ordering = ("-created_at", "-id")
