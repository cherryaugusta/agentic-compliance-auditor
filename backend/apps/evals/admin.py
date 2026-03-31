from django.contrib import admin

from apps.evals.models import EvalCase, EvalRun


@admin.register(EvalCase)
class EvalCaseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "dataset_name",
        "scenario_type",
        "is_adversarial",
        "input_bundle_path",
        "created_at",
    )
    list_filter = ("dataset_name", "scenario_type", "is_adversarial", "created_at")
    search_fields = ("dataset_name", "scenario_type", "input_bundle_path")
    ordering = ("-created_at", "-id")


@admin.register(EvalRun)
class EvalRunAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "run_label",
        "status",
        "started_at",
        "finished_at",
        "created_at",
    )
    list_filter = ("status", "created_at", "started_at", "finished_at")
    search_fields = ("run_label",)
    ordering = ("-created_at", "-id")
