from django.db import models

from apps.core.models import TimeStampedModel
from apps.documents.models import PolicyDocument


class DocumentLineage(TimeStampedModel):
    class RelationshipType(models.TextChoices):
        SUPERSEDES = "supersedes", "Supersedes"
        DERIVED_FROM = "derived_from", "Derived From"
        REFERENCES = "references", "References"
        IMPLEMENTS = "implements", "Implements"
        ALIGNED_TO = "aligned_to", "Aligned To"

    parent_document = models.ForeignKey(
        PolicyDocument, on_delete=models.CASCADE, related_name="child_lineage_links"
    )
    child_document = models.ForeignKey(
        PolicyDocument, on_delete=models.CASCADE, related_name="parent_lineage_links"
    )
    relationship_type = models.CharField(max_length=32, choices=RelationshipType.choices)

    class Meta:
        unique_together = ("parent_document", "child_document", "relationship_type")
