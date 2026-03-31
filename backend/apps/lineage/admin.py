from django.contrib import admin

from apps.lineage.models import DocumentLineage


@admin.register(DocumentLineage)
class DocumentLineageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "parent_document",
        "child_document",
        "relationship_type",
        "created_at",
    )
    list_filter = ("relationship_type", "created_at")
    search_fields = (
        "parent_document__title",
        "child_document__title",
        "relationship_type",
    )
    ordering = ("-created_at", "-id")
