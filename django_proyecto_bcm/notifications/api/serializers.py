from datetime import datetime, timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from notifications.models import Notification


class NotificationSerializer(ModelSerializer):
    days = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields=[
            "id",
            "title",
            "description",
            "read",
            "date",
            "users",
            "days",
        ]
        extra_kwargs={
            "date": {"read_only": True},
            "users": {"read_only": True},
        }

    def get_days(self, obj):
        days = (datetime.now(timezone.utc)-obj.date).days
        return days