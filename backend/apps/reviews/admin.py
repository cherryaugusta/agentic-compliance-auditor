from django.contrib import admin

from apps.reviews.models import ReviewerAction, ReviewTask


@admin.register(ReviewTask)
class ReviewTaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "conflict_flag",
        "queue_name",
        "assigned_to",
        "status",
        "reason_code",
        "sla_due_at",
        "created_at",
    )
    list_filter = ("status", "queue_name", "reason_code", "sla_due_at", "created_at")
    search_fields = (
        "queue_name",
        "assigned_to__username",
        "conflict_flag__reason_summary",
    )
    ordering = ("sla_due_at", "-id")


@admin.register(ReviewerAction)
class ReviewerActionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "review_task",
        "reviewer",
        "action_type",
        "override_reason_code",
        "created_at",
    )
    list_filter = ("action_type", "created_at")
    search_fields = (
        "reviewer__username",
        "comment",
        "override_reason_code",
        "review_task__conflict_flag__reason_summary",
    )
    ordering = ("-created_at", "-id")
