from datetime import datetime, timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from notifications.models import Notification


class NotificationSerializer(ModelSerializer):
    days = serializers.SerializerMethodField()
    type_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Notification
        fields=[
            "id",
            "title",
            "description",
            "type",
            "type_name",
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
        days = (datetime.now(timezone.utc).replace(tzinfo=None)-obj.date).days
        return days
        
    def get_type_name(self, obj):
        return dict(Notification.TYPE).get(obj.type)