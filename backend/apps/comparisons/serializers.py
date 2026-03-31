from rest_framework import serializers

from apps.comparisons.models import ComparisonRun


class ComparisonRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComparisonRun
        fields = "__all__"
