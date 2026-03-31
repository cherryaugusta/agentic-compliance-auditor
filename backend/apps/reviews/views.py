from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.audits.models import AuditEvent
from apps.findings.models import ConflictFlag
from apps.reviews.models import ReviewerAction, ReviewTask
from apps.reviews.serializers import ReviewTaskSerializer


def _audit(request, task: ReviewTask, event_type: str, payload: dict):
    AuditEvent.objects.create(
        entity_type="ReviewTask",
        entity_id=str(task.id),
        event_type=event_type,
        actor_type=AuditEvent.ActorType.REVIEWER,
        actor_id=(
            str(getattr(request.user, "id", ""))
            if getattr(request, "user", None) and request.user.is_authenticated
            else None
        ),
        correlation_id=getattr(request, "correlation_id", "review-action"),
        payload=payload,
    )


class ReviewTaskViewSet(viewsets.ModelViewSet):
    queryset = (
        ReviewTask.objects.select_related("conflict_flag", "assigned_to")
        .all()
        .order_by("sla_due_at", "-id")
    )
    serializer_class = ReviewTaskSerializer

    @action(detail=True, methods=["post"])
    def assign(self, request, pk=None):
        task = self.get_object()
        username = request.data.get("username", "reviewer1")
        user = get_user_model().objects.filter(username=username).first()
        task.assigned_to = user
        task.status = ReviewTask.Status.ASSIGNED
        task.save(update_fields=["assigned_to", "status"])
        ReviewerAction.objects.create(
            review_task=task,
            reviewer=user or get_user_model().objects.first(),
            action_type=ReviewerAction.ActionType.REQUEST_UPDATE,
            comment=f"Assigned to {username}.",
        )
        _audit(request, task, "review_task_assigned", {"username": username})
        return Response(self.get_serializer(task).data)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        task = self.get_object()
        task.status = ReviewTask.Status.APPROVED
        task.save(update_fields=["status"])
        task.conflict_flag.status = ConflictFlag.Status.CONFIRMED
        task.conflict_flag.save(update_fields=["status"])
        reviewer = task.assigned_to or get_user_model().objects.first()
        ReviewerAction.objects.create(
            review_task=task,
            reviewer=reviewer,
            action_type=ReviewerAction.ActionType.APPROVE,
            comment=request.data.get("comment", "Approved."),
        )
        _audit(
            request, task, "review_task_approved", {"conflict_status": task.conflict_flag.status}
        )
        return Response(self.get_serializer(task).data)

    @action(detail=True, methods=["post"])
    def override(self, request, pk=None):
        task = self.get_object()
        task.status = ReviewTask.Status.OVERRIDDEN
        task.save(update_fields=["status"])
        task.conflict_flag.status = ConflictFlag.Status.DISMISSED
        task.conflict_flag.save(update_fields=["status"])
        reviewer = task.assigned_to or get_user_model().objects.first()
        ReviewerAction.objects.create(
            review_task=task,
            reviewer=reviewer,
            action_type=ReviewerAction.ActionType.OVERRIDE,
            comment=request.data.get("comment", "Overridden."),
            override_reason_code=request.data.get("override_reason_code", "manual_override"),
        )
        _audit(
            request, task, "review_task_overridden", {"conflict_status": task.conflict_flag.status}
        )
        return Response(self.get_serializer(task).data)

    @action(detail=True, methods=["post"])
    def dismiss(self, request, pk=None):
        task = self.get_object()
        task.status = ReviewTask.Status.DISMISSED
        task.save(update_fields=["status"])
        task.conflict_flag.status = ConflictFlag.Status.DISMISSED
        task.conflict_flag.save(update_fields=["status"])
        reviewer = task.assigned_to or get_user_model().objects.first()
        ReviewerAction.objects.create(
            review_task=task,
            reviewer=reviewer,
            action_type=ReviewerAction.ActionType.DISMISS,
            comment=request.data.get("comment", "Dismissed."),
        )
        _audit(
            request, task, "review_task_dismissed", {"conflict_status": task.conflict_flag.status}
        )
        return Response(self.get_serializer(task).data)

    @action(detail=True, methods=["post"])
    def escalate(self, request, pk=None):
        task = self.get_object()
        task.status = ReviewTask.Status.ESCALATED
        task.save(update_fields=["status"])
        task.conflict_flag.status = ConflictFlag.Status.ESCALATED
        task.conflict_flag.save(update_fields=["status"])
        reviewer = task.assigned_to or get_user_model().objects.first()
        ReviewerAction.objects.create(
            review_task=task,
            reviewer=reviewer,
            action_type=ReviewerAction.ActionType.ESCALATE,
            comment=request.data.get("comment", "Escalated."),
        )
        _audit(
            request, task, "review_task_escalated", {"conflict_status": task.conflict_flag.status}
        )
        return Response(self.get_serializer(task).data, status=status.HTTP_200_OK)
