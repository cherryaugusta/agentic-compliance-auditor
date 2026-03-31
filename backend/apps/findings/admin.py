from django.contrib import admin

from apps.findings.models import ConflictFlag, EvidenceCitation, FindingMemo


@admin.register(ConflictFlag)
class ConflictFlagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "comparison_run",
        "conflict_type",
        "severity",
        "status",
        "confidence",
        "requires_review",
        "created_at",
    )
    list_filter = (
        "conflict_type",
        "severity",
        "status",
        "requires_review",
        "created_at",
    )
    search_fields = (
        "reason_summary",
        "source_statement__document__title",
        "target_statement__document__title",
        "model_version",
    )
    ordering = ("-created_at", "-id")


@admin.register(EvidenceCitation)
class EvidenceCitationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "conflict_flag",
        "document",
        "section",
        "citation_role",
        "created_at",
    )
    list_filter = ("citation_role", "created_at")
    search_fields = (
        "document__title",
        "excerpt_text",
        "conflict_flag__reason_summary",
    )
    ordering = ("-created_at", "-id")


@admin.register(FindingMemo)
class FindingMemoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "conflict_flag",
        "recommended_action",
        "confidence",
        "prompt_version",
        "created_at",
    )
    list_filter = ("recommended_action", "created_at")
    search_fields = ("summary", "conflict_flag__reason_summary")
    ordering = ("-created_at", "-id")
