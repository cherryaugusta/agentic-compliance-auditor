from django.conf import settings
from django.db import models
from pgvector.django import VectorField

from apps.core.models import TimeStampedModel
from apps.documents.models import DocumentSection, PolicyDocument


class ControlStatement(TimeStampedModel):
    class StatementType(models.TextChoices):
        OBLIGATION = "obligation", "Obligation"
        CONTROL = "control", "Control"
        PROCEDURE_STEP = "procedure_step", "Procedure Step"
        TIMELINE = "timeline", "Timeline"
        THRESHOLD = "threshold", "Threshold"
        EXCEPTION_RULE = "exception_rule", "Exception Rule"
        APPROVAL_RULE = "approval_rule", "Approval Rule"

    document = models.ForeignKey(
        PolicyDocument, on_delete=models.CASCADE, related_name="statements"
    )
    section = models.ForeignKey(
        DocumentSection, on_delete=models.CASCADE, related_name="statements"
    )
    statement_type = models.CharField(max_length=32, choices=StatementType.choices)
    raw_text = models.TextField()
    normalized_text = models.TextField()
    subject_entity = models.CharField(max_length=255, blank=True, null=True)
    action_verb = models.CharField(max_length=255, blank=True, null=True)
    condition_text = models.TextField(blank=True, null=True)
    deadline_text = models.CharField(max_length=255, blank=True, null=True)
    threshold_text = models.CharField(max_length=255, blank=True, null=True)
    owner_role = models.CharField(max_length=255, blank=True, null=True)
    schema_valid = models.BooleanField(default=True)
    extraction_confidence = models.FloatField(default=0.0)
    extraction_version = models.CharField(max_length=50, default="v1")
    embedding = VectorField(dimensions=settings.PGVECTOR_DIMENSIONS, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["document", "statement_type"]),
        ]
