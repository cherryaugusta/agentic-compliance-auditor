from django.db import models

from apps.core.models import TimeStampedModel
from apps.documents.models import PolicyDocument


class ComparisonRun(TimeStampedModel):
    class RunType(models.TextChoices):
        VERSION_DIFF = "version_diff", "Version Diff"
        INTERNAL_VS_EXTERNAL = "internal_vs_external", "Internal vs External"
        POLICY_VS_CONTROL = "policy_vs_control", "Policy vs Control"
        CROSS_DOCUMENT = "cross_document", "Cross Document"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        RUNNING = "running", "Running"
        COMPLETED = "completed", "Completed"
        DEGRADED = "degraded", "Degraded"
        FAILED = "failed", "Failed"

    source_document = models.ForeignKey(
        PolicyDocument, on_delete=models.CASCADE, related_name="comparison_sources"
    )
    run_type = models.CharField(max_length=32, choices=RunType.choices)
    target_document_ids = models.JSONField(default=list)
    config_snapshot = models.JSONField(default=dict)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    correlation_id = models.CharField(max_length=64)
