from rest_framework import serializers

from apps.documents.models import DocumentSection, PolicyDocument
from apps.statements.models import ControlStatement


class DocumentSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentSection
        fields = "__all__"


class ControlStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControlStatement
        fields = "__all__"


class PolicyDocumentSerializer(serializers.ModelSerializer):
    section_count = serializers.IntegerField(source="sections.count", read_only=True)
    statement_count = serializers.IntegerField(source="statements.count", read_only=True)

    class Meta:
        model = PolicyDocument
        fields = "__all__"
