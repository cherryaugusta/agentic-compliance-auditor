from django.db import models

from apps.core.models import TimeStampedModel


class PolicyDocument(TimeStampedModel):
    class DocumentType(models.TextChoices):
        INTERNAL_POLICY = "internal_policy", "Internal Policy"
        PROCEDURE = "procedure", "Procedure"
        CONTROL_LIBRARY = "control_library", "Control Library"
        GUIDANCE = "guidance", "Guidance"
        STANDARD = "standard", "Standard"
        BOARD_PAPER = "board_paper", "Board Paper"

    class DomainArea(models.TextChoices):
        COMPLAINTS = "complaints", "Complaints"
        CONSUMER_SUPPORT = "consumer_support", "Consumer Support"
        COMMUNICATIONS = "communications", "Communications"
        ESCALATIONS = "escalations", "Escalations"
        GOVERNANCE = "governance", "Governance"
        VULNERABLE_CUSTOMERS = "vulnerable_customers", "Vulnerable Customers"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        ACTIVE = "active", "Active"
        RETIRED = "retired", "Retired"
        ARCHIVED = "archived", "Archived"

    document_type = models.CharField(max_length=32, choices=DocumentType.choices)
    title = models.CharField(max_length=255)
    source_name = models.CharField(max_length=255)
    jurisdiction = models.CharField(max_length=100, blank=True, null=True)
    domain_area = models.CharField(
        max_length=32, choices=DomainArea.choices, default=DomainArea.OTHER
    )
    owner_team = models.CharField(max_length=255, blank=True, null=True)
    version_label = models.CharField(max_length=50)
    effective_date = models.DateField()
    supersedes_document = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="superseded_by"
    )
    is_external_source = models.BooleanField(default=False)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
    storage_path = models.CharField(max_length=500)
    sha256_checksum = models.CharField(max_length=64, db_index=True)
    content_text = models.TextField(default="")

    class Meta:
        indexes = [
            models.Index(fields=["document_type", "domain_area", "status", "effective_date"]),
        ]

    def __str__(self):
        return f"{self.title} {self.version_label}"


class DocumentSection(TimeStampedModel):
    document = models.ForeignKey(PolicyDocument, on_delete=models.CASCADE, related_name="sections")
    section_index = models.PositiveIntegerField()
    heading = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField()
    char_start = models.PositiveIntegerField(default=0)
    char_end = models.PositiveIntegerField(default=0)
    page_number = models.PositiveIntegerField(blank=True, null=True)
    parser_confidence = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ["section_index"]
