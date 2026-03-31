from django.db import models

from apps.comparisons.models import ComparisonRun
from apps.core.models import TimeStampedModel
from apps.documents.models import DocumentSection, PolicyDocument
from apps.observability.models import PromptVersion
from apps.statements.models import ControlStatement


class ConflictFlag(TimeStampedModel):
    class ConflictType(models.TextChoices):
        DIRECT_CONTRADICTION = "direct_contradiction", "Direct Contradiction"
        WEAKER_INTERNAL_CONTROL = "weaker_internal_control", "Weaker Internal Control"
        MISSING_CONTROL = "missing_control", "Missing Control"
        STALE_REFERENCE = "stale_reference", "Stale Reference"
        THRESHOLD_CONFLICT = "threshold_conflict", "Threshold Conflict"
        TIMELINE_CONFLICT = "timeline_conflict", "Timeline Conflict"
        APPROVAL_CONFLICT = "approval_conflict", "Approval Conflict"
        TERMINOLOGY_DRIFT = "terminology_drift", "Terminology Drift"
        COVERAGE_GAP = "coverage_gap", "Coverage Gap"

    class Severity(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical"

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        NEEDS_REVIEW = "needs_review", "Needs Review"
        DISMISSED = "dismissed", "Dismissed"
        CONFIRMED = "confirmed", "Confirmed"
        ESCALATED = "escalated", "Escalated"
        RESOLVED = "resolved", "Resolved"

    comparison_run = models.ForeignKey(
        ComparisonRun, on_delete=models.CASCADE, related_name="conflicts"
    )
    source_statement = models.ForeignKey(
        ControlStatement, on_delete=models.CASCADE, related_name="source_conflicts"
    )
    target_statement = models.ForeignKey(
        ControlStatement,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="target_conflicts",
    )
    conflict_type = models.CharField(max_length=32, choices=ConflictType.choices)
    severity = models.CharField(max_length=16, choices=Severity.choices)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.OPEN)
    confidence = models.FloatField(default=0.0)
    requires_review = models.BooleanField(default=True)
    reason_summary = models.TextField()
    rules_triggered = models.JSONField(default=list)
    model_version = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["status", "severity", "conflict_type", "created_at"]),
        ]


class EvidenceCitation(TimeStampedModel):
    class CitationRole(models.TextChoices):
        SOURCE = "source", "Source"
        TARGET = "target", "Target"
        CONTEXT = "context", "Context"

    conflict_flag = models.ForeignKey(
        ConflictFlag, on_delete=models.CASCADE, related_name="citations"
    )
    document = models.ForeignKey(PolicyDocument, on_delete=models.CASCADE)
    section = models.ForeignKey(DocumentSection, on_delete=models.CASCADE)
    citation_role = models.CharField(max_length=16, choices=CitationRole.choices)
    excerpt_text = models.TextField()


class FindingMemo(TimeStampedModel):
    class RecommendedAction(models.TextChoices):
        REVIEW = "review", "Review"
        CONFIRM = "confirm", "Confirm"
        DISMISS = "dismiss", "Dismiss"
        ESCALATE = "escalate", "Escalate"
        REQUEST_POLICY_UPDATE = "request_policy_update", "Request Policy Update"

    conflict_flag = models.OneToOneField(
        ConflictFlag, on_delete=models.CASCADE, related_name="memo"
    )
    recommended_action = models.CharField(max_length=32, choices=RecommendedAction.choices)
    summary = models.TextField()
    structured_rationale = models.JSONField(default=dict)
    confidence = models.FloatField(default=0.0)
    prompt_version = models.ForeignKey(
        PromptVersion, on_delete=models.SET_NULL, null=True, blank=True, related_name="memos"
    )
