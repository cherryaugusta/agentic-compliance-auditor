from rest_framework import serializers

from apps.findings.models import ConflictFlag, EvidenceCitation, FindingMemo


class EvidenceCitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvidenceCitation
        fields = "__all__"


class FindingMemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FindingMemo
        fields = "__all__"


class ConflictFlagSerializer(serializers.ModelSerializer):
    citation_count = serializers.IntegerField(source="citations.count", read_only=True)
    has_memo = serializers.SerializerMethodField()

    class Meta:
        model = ConflictFlag
        fields = "__all__"

    def get_has_memo(self, obj):
        return hasattr(obj, "memo")
