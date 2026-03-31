from django.contrib import admin

from apps.statements.models import ControlStatement


@admin.register(ControlStatement)
class ControlStatementAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "document",
        "statement_type",
        "owner_role",
        "schema_valid",
        "extraction_confidence",
        "extraction_version",
        "created_at",
    )
    list_filter = ("statement_type", "schema_valid", "extraction_version", "created_at")
    search_fields = (
        "document__title",
        "raw_text",
        "normalized_text",
        "subject_entity",
        "action_verb",
        "owner_role",
    )
    ordering = ("-created_at", "-id")
