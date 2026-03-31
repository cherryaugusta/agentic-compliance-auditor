from django.db import models

from apps.comparisons.models import ComparisonRun
from apps.core.models import TimeStampedModel
from apps.documents.models import PolicyDocument


class GuidanceSource(TimeStampedModel):
    class SourceType(models.TextChoices):
        FCA_GUIDANCE = "fca_guidance", "FCA Guidance"
        INDUSTRY_STANDARD = "industry_standard", "Industry Standard"
        INTERNAL_STANDARD = "internal_standard", "Internal Standard"
        BOARD_STANDARD = "board_standard", "Board Standard"

    document = models.OneToOneField(
        PolicyDocument, on_delete=models.CASCADE, related_name="guidance_source"
    )
    source_type = models.CharField(max_length=32, choices=SourceType.choices)
    reference_code = models.CharField(max_length=100, blank=True, null=True)
    effective_date = models.DateField()
    active = models.BooleanField(default=True)


class PromptVersion(TimeStampedModel):
    class Purpose(models.TextChoices):
        SECTIONING = "sectioning", "Sectioning"
        STATEMENT_EXTRACTION = "statement_extraction", "Statement Extraction"
        CONTRADICTION_ANALYSIS = "contradiction_analysis", "Contradiction Analysis"
        MEMO_GENERATION = "memo_generation", "Memo Generation"

    name = models.CharField(max_length=255)
    version_label = models.CharField(max_length=50)
    purpose = models.CharField(max_length=32, choices=Purpose.choices)
    template_text = models.TextField()
    schema_version = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)


class ModelExecutionLog(TimeStampedModel):
    class Status(models.TextChoices):
        SUCCESS = "success", "Success"
        TIMEOUT = "timeout", "Timeout"
        SCHEMA_FAIL = "schema_fail", "Schema Fail"
        PROVIDER_ERROR = "provider_error", "Provider Error"
        FALLBACK_USED = "fallback_used", "Fallback Used"

    comparison_run = models.ForeignKey(
        ComparisonRun, on_delete=models.SET_NULL, null=True, blank=True, related_name="model_logs"
    )
    task_name = models.CharField(max_length=255)
    provider_name = models.CharField(max_length=255)
    model_name = models.CharField(max_length=255)
    prompt_version = models.ForeignKey(
        PromptVersion, on_delete=models.SET_NULL, null=True, blank=True, related_name="executions"
    )
    latency_ms = models.PositiveIntegerField(default=0)
    input_token_estimate = models.PositiveIntegerField(default=0)
    output_token_estimate = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=32, choices=Status.choices)
    cost_estimate = models.DecimalField(max_digits=10, decimal_places=4, default=0)
