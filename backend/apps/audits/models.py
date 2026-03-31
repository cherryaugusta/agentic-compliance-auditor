from django.db import models

from apps.core.models import TimeStampedModel


class AuditEvent(TimeStampedModel):
    class ActorType(models.TextChoices):
        SYSTEM = "system", "System"
        USER = "user", "User"
        REVIEWER = "reviewer", "Reviewer"
        JOB = "job", "Job"

    entity_type = models.CharField(max_length=100)
    entity_id = models.CharField(max_length=64)
    event_type = models.CharField(max_length=100)
    actor_type = models.CharField(max_length=16, choices=ActorType.choices)
    actor_id = models.CharField(max_length=64, blank=True, null=True)
    correlation_id = models.CharField(max_length=64)
    payload = models.JSONField(default=dict)

    class Meta:
        indexes = [
            models.Index(fields=["entity_type", "entity_id", "created_at"]),
        ]
