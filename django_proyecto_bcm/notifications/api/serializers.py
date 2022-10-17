from datetime import datetime, timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from notifications.models import Notification, N_U


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




class N_USerializer(serializers.ModelSerializer):
    notification_title = serializers.CharField(read_only=True, source="notification.title")
    notification_description = serializers.CharField(read_only=True, source="notification.description")
    notification_type = serializers.IntegerField(read_only = True,source="notification.type")
    notification_type_name =serializers.SerializerMethodField(read_only=True, source="notification.type")
    notification_days = serializers.SerializerMethodField()
    notification_date = serializers.CharField(read_only=True, source="notification.date")
    
    class Meta:
        model = N_U
        fields = [
            'id',
            'read',
            'notification_title',
            'notification_description',
            'notification_type',
            'notification_type_name',
            'notification_days',
            'notification_date',
        ] 

    def get_notification_type_name(self,obj):
        return dict(Notification.TYPE).get(obj.notification.type)

    def get_notification_days(self, obj):
        days = (datetime.now(timezone.utc).replace(tzinfo=None)-obj.notification.date).days
        return days
        