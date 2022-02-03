from bcm_phase2.models import ServiceOffered
from rest_framework import serializers
from django.db.models import F, Q


class ServiceOfferedListSerializer(serializers.ModelSerializer):
    type_name = serializers.SerializerMethodField(read_only=True)
    area_name = serializers.CharField(read_only=True)
    scale_max_value = serializers.CharField(read_only=True)

    class Meta:
        model = ServiceOffered
        fields = [
            'id',
            'name',
            'type',
            'type_name',
            'profit',
            'recovery_time',
            'criticality',
            'area_name',
            'scale_max_value',
        ]

    def get_type_name(self, obj):
        return dict(ServiceOffered.TYPE).get(obj.type)


class ServiceOfferedSerializer(serializers.ModelSerializer):
    type_name = serializers.SerializerMethodField(read_only=True)
    area_name = serializers.CharField(read_only=True)
    scale_name = serializers.CharField(read_only=True)
    scale_min_value = serializers.CharField(read_only=True)
    scale_max_value = serializers.CharField(read_only=True)

    class Meta:
        model = ServiceOffered
        fields = [
            'id',
            'name',
            'type',
            'type_name',
            'profit',
            'recovery_time',
            'criticality',
            'area',
            'area_name',
            'scale',
            'scale_name',
            'scale_min_value',
            'scale_max_value',
        ]

    def get_type_name(self, obj):
        return dict(ServiceOffered.TYPE).get(obj.type)
