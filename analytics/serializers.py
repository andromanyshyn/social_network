from rest_framework import serializers

from analytics.models import PostActivity


class PostActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostActivity
        fields = ("user", "post", "action", "occurred_at")
