from django.db import models

from apps.core.models import TimeStampedModel


class EvalCase(TimeStampedModel):
    dataset_name = models.CharField(max_length=100)
    scenario_type = models.CharField(max_length=100)
    input_bundle_path = models.CharField(max_length=500)
    ground_truth = models.JSONField(default=dict)
    is_adversarial = models.BooleanField(default=False)


class EvalRun(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        RUNNING = "running", "Running"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    run_label = models.CharField(max_length=100)
    config_snapshot = models.JSONField(default=dict)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    summary_metrics = models.JSONField(default=dict)
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)
