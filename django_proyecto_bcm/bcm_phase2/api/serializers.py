from bcm_phase2.models import ServiceOffered, ServiceUsed
from rest_framework import serializers
from django.db.models import F, Q
from bcm_phase1.api.serializers import RiskSerializer


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
            'area',
            'area_name',
            'scale',
            'scale_max_value',
        ]

    def get_type_name(self, obj):
        return dict(ServiceOffered.TYPE).get(obj.type)


class ServiceOfferedSerializer(serializers.ModelSerializer):
    type_name = serializers.SerializerMethodField(read_only=True)
    area_name = serializers.CharField(read_only=True, source="area.name")
    scale_name = serializers.CharField(read_only=True, source="scale.name")
    scale_min_value = serializers.CharField(
        read_only=True, source="scale.min_value")
    scale_max_value = serializers.CharField(
        read_only=True, source="scale.max_value")

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


class ServiceUsedListSerializer(serializers.ModelSerializer):
    scale_max_value = serializers.CharField(read_only=True)

    class Meta:
        model = ServiceUsed
        fields = [
            'id',
            'name',
            'spending',
            'recovery_time',
            'criticality',
            'scale',
            'scale_max_value',
        ]


class ServiceUsedSerializer(serializers.ModelSerializer):
    scale_name = serializers.CharField(read_only=True)
    scale_min_value = serializers.CharField(read_only=True)
    scale_max_value = serializers.CharField(read_only=True)
    # El service_offered funciona para llenar los elementos del many to many
    services_offered = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True)
    # Serializer aninado
    _services_offered = ServiceOfferedSerializer(many=True, read_only=True)
    # El risks funciona para llenar los elementos del many to many
    risks = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True)
    # Serializer aninado
    _risks = RiskSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceUsed
        fields = [
            'id',
            'name',
            'spending',
            'recovery_time',
            'criticality',
            'scale',
            'scale_name',
            'scale_min_value',
            'scale_max_value',
            'services_offered',
            '_services_offered',
            'risks',
            '_risks'
        ]
