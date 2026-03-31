from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel
from apps.findings.models import ConflictFlag


class ReviewTask(TimeStampedModel):
    class Status(models.TextChoices):
        UNASSIGNED = "unassigned", "Unassigned"
        ASSIGNED = "assigned", "Assigned"
        IN_REVIEW = "in_review", "In Review"
        APPROVED = "approved", "Approved"
        OVERRIDDEN = "overridden", "Overridden"
        DISMISSED = "dismissed", "Dismissed"
        ESCALATED = "escalated", "Escalated"
        CLOSED = "closed", "Closed"

    class ReasonCode(models.TextChoices):
        LOW_CONFIDENCE = "low_confidence", "Low Confidence"
        HIGH_SEVERITY = "high_severity", "High Severity"
        SCHEMA_FAILURE = "schema_failure", "Schema Failure"
        STALE_REFERENCE = "stale_reference", "Stale Reference"
        MISSING_CONTROL = "missing_control", "Missing Control"
        MANUAL_SAMPLING = "manual_sampling", "Manual Sampling"
        PROVIDER_FAILURE = "provider_failure", "Provider Failure"

    conflict_flag = models.OneToOneField(
        ConflictFlag, on_delete=models.CASCADE, related_name="review_task"
    )
    queue_name = models.CharField(max_length=100)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="review_tasks",
    )
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.UNASSIGNED)
    reason_code = models.CharField(max_length=32, choices=ReasonCode.choices)
    sla_due_at = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=["status", "queue_name", "sla_due_at"]),
        ]


class ReviewerAction(TimeStampedModel):
    class ActionType(models.TextChoices):
        APPROVE = "approve", "Approve"
        OVERRIDE = "override", "Override"
        DISMISS = "dismiss", "Dismiss"
        ESCALATE = "escalate", "Escalate"
        REQUEST_UPDATE = "request_update", "Request Update"
        MARK_FALSE_POSITIVE = "mark_false_positive", "Mark False Positive"
        CLOSE = "close", "Close"

    review_task = models.ForeignKey(ReviewTask, on_delete=models.CASCADE, related_name="actions")
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=32, choices=ActionType.choices)
    old_value = models.JSONField(blank=True, null=True)
    new_value = models.JSONField(blank=True, null=True)
    comment = models.TextField()
    override_reason_code = models.CharField(max_length=100, blank=True, null=True)
