from rest_framework import serializers

from apps.reviews.models import ReviewerAction, ReviewTask


class ReviewerActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewerAction
        fields = "__all__"


class ReviewTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewTask
        fields = "__all__"
