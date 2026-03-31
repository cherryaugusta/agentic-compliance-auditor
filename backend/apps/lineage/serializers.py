from rest_framework import serializers

from apps.lineage.models import DocumentLineage


class DocumentLineageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentLineage
        fields = "__all__"
