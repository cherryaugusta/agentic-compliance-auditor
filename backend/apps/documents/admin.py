from django.contrib import admin

from apps.documents.models import DocumentSection, PolicyDocument


@admin.register(PolicyDocument)
class PolicyDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "document_type",
        "version_label",
        "status",
        "domain_area",
        "effective_date",
        "source_name",
        "is_external_source",
    )
    list_filter = ("document_type", "status", "domain_area", "is_external_source", "effective_date")
    search_fields = ("title", "version_label", "source_name", "owner_team", "sha256_checksum")
    ordering = ("-effective_date", "-id")


@admin.register(DocumentSection)
class DocumentSectionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "document",
        "section_index",
        "heading",
        "page_number",
        "parser_confidence",
    )
    list_filter = ("page_number",)
    search_fields = ("document__title", "heading", "text")
    ordering = ("document", "section_index")
