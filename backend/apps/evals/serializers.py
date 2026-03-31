from rest_framework import serializers

from apps.evals.models import EvalCase, EvalRun


class EvalCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvalCase
        fields = "__all__"


class EvalRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvalRun
        fields = "__all__"
