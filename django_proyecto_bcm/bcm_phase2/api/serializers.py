from bcm_phase2.models import ServiceOffered, ServiceUsed, Staff, InterestedParty,OrganizationActivity
from rest_framework import serializers
from django.db.models import F, Q
from bcm_phase1.api.serializers import RiskSerializer
from configuration.api.serializers import HeadquarterSerializer


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


class StaffListSerializer(serializers.ModelSerializer):
    area_name = serializers.CharField(read_only=True)
    position_name = serializers.CharField(read_only=True)

    class Meta:
        model = Staff
        fields = [
            'id',
            'staff_number',
            'names',
            'surnames',
            'earnings',
            'area',
            'area_name',
            'position',
            'position_name',
        ]


class StaffSerializer(serializers.ModelSerializer):
    area_name = serializers.CharField(read_only=True)
    position_name = serializers.CharField(read_only=True)
    headquarter_name = serializers.CharField(read_only=True)
    user_email = serializers.CharField(read_only=True)

    class Meta:
        model = Staff
        fields = [
            'id',
            'staff_number',
            'names',
            'surnames',
            'earnings',
            'area',
            'area_name',
            'position',
            'position_name',
            'headquarter',
            'headquarter_name',
            'user',
            'user_email'
        ]

class OrganizationActivityListSerializer(serializers.ModelSerializer):
    scale_max_value = serializers.CharField(read_only=True)

    class Meta:
        model = OrganizationActivity
        fields =[
            'id',
            'name',
            'description',
            'cost',
            'recovery_time',
            'criticality',
            'scale',
            'scale_max_value'
        ]

class OrganizationActivitySerializer(serializers.ModelSerializer):
    scale_name = serializers.CharField(read_only=True)
    scale_min_value = serializers.CharField(read_only=True, source="scale.min_value")
    scale_max_value = serializers.CharField(read_only=True, source="scale.max_value")
    
    services_offered = serializers.ListField(
        child=serializers.IntegerField(),required=False,write_only=True)
    _services_offered = ServiceOfferedSerializer(many=True,read_only=True)

    risks = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True)
    _risks = RiskSerializer(many=True, read_only=True)
    
    headquarters = serializers.ListField(
        child=serializers.IntegerField(),required=False,write_only=True)
    _headquarters = HeadquarterSerializer(many=True,read_only=True)

    class Meta:
        model = OrganizationActivity
        fields = [
            'id',
            'name',
            'description',
            'cost',
            'recovery_time',
            'criticality',
            'services_offered',
            '_services_offered',
            'scale',
            'scale_name',
            'scale_min_value',
            'scale_max_value',
            'risks',
            '_risks',
            'headquarters',
            '_headquarters',

        ]


class InterestedPartyListSerializer(serializers.ModelSerializer):
    type_name = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = InterestedParty
        fields =[
            'id',
            'name',
            'type',
            'type_name',
            'description'
        ]

class interestedPartySerializer(serializers.ModelSerializer):
    type_name = serializers.SerializerMethodField(read_only = True)
    organization_name = serializers.CharField(read_only = True, source="organization.name")

    class Meta:
        model = InterestedParty
        fields = [
            'id',
            'name',
            'type',
            'type_name',
            'description',
            'organization',
            'organization_name'
        ] 