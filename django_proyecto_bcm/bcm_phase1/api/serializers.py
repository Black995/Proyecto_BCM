from bcm_phase1.models import Risk, CrisisScenario
from rest_framework import serializers
from django.db.models import F, Q

"""
    Funciones utilizadas para el importe de los serializers con el fin de evitar
    problemas de recursividad de archivos
"""
def service_offered_list_serializer():
    from bcm_phase2.api.serializers import ServiceOfferedListSerializer
    return ServiceOfferedListSerializer

def service_used_list_serializer():
    from bcm_phase2.api.serializers import ServiceUsedListSerializer
    return ServiceUsedListSerializer

def organization_activity_list_serializer():
    from bcm_phase2.api.serializers import OrganizationActivityListSerializer
    return OrganizationActivityListSerializer


class RiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risk
        fields = [
            'id',
            'name',
            'description',
        ]




class CrisisScenarioSerializer(serializers.ModelSerializer):
    # El risks funciona para llenar los elementos del many to many
    risks = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True)
    # Serializer aninado
    _risks = RiskSerializer(many=True, read_only=True)

    class Meta:
        model = CrisisScenario
        fields = [
            'id',
            'name',
            'description',
            'risks',
            '_risks',
        ]



class CrisisScenarioListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CrisisScenario
        fields = [
            'id',
            'name',
            'description',
        ]


"""
    Queries para la fase 3 del BCM
"""

class ServicesOfferedRiskSerializer(serializers.ModelSerializer):
    # Serializer aninado
    services_offered_risk = service_offered_list_serializer()(many=True, read_only=True, source='risk_service_offered')

    class Meta:
        model = Risk
        fields = [
            'id',
            'name',
            'services_offered_risk'
        ]

class ServicesUsedRiskSerializer(serializers.ModelSerializer):
    # Serializer aninado
    services_used_risk = service_used_list_serializer()(many=True, read_only=True, source='risk_service_used')

    class Meta:
        model = Risk
        fields = [
            'id',
            'name',
            'services_used_risk'
        ]

class OrganizationActivitiesRiskSerializer(serializers.ModelSerializer):
    # Serializer aninado
    organization_activities_risk = organization_activity_list_serializer()(many=True, read_only=True, source='risk_organizacion_activity')

    class Meta:
        model = Risk
        fields = [
            'id',
            'name',
            'organization_activities_risk'
        ]

