from bcm_phase3.models import IncidentHistory
from bcm_phase1.models import CrisisScenario, Risk
from rest_framework import serializers
from django.db.models import F, Q
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from bcm_phase1.api.serializers import (RiskSerializer, ServicesOfferedRiskSerializer, 
                                        ServicesUsedRiskSerializer, OrganizationActivitiesRiskSerializer)



class IncidentHistoryListSerializer(serializers.ModelSerializer):
    crisis_scenario_name = serializers.CharField(read_only=True, source="crisis_scenario.name")
    
    class Meta:
        model = IncidentHistory
        fields = [
            'id',
            'start_date',
            'end_date',
            'description',
            'crisis_scenario',
            'crisis_scenario_name',
        ]



class IncidentHistorySerializer(serializers.ModelSerializer):
    crisis_scenario_name = serializers.CharField(read_only=True, source="crisis_scenario.name")
    crisis_scenario_description = serializers.CharField(read_only=True, source="crisis_scenario.description")
    
    class Meta:
        model = IncidentHistory
        fields = [
            'id',
            'start_date',
            'end_date',
            'description',
            'crisis_scenario',
            'crisis_scenario_name',
            'crisis_scenario_description'
        ]


class RisksAffectedByIncidentSerializer(serializers.ModelSerializer):
    crisis_scenario_name = serializers.CharField(read_only=True, source="crisis_scenario.name")
    # Serializer aninado
    risks_incident = RiskSerializer(many=True, read_only=True, source='crisis_scenario._risks')
    
    class Meta:
        model = IncidentHistory
        fields = [
            'id',
            'start_date',
            'end_date',
            'crisis_scenario_name',
            'risks_incident'
        ]


class ServicesOfferedAffectedByIncidentSerializer(serializers.ModelSerializer):
    crisis_scenario_name = serializers.CharField(read_only=True, source="crisis_scenario.name")
    # Serializer aninado
    risks_incident = ServicesOfferedRiskSerializer(many=True, read_only=True, source='crisis_scenario._risks')
    
    class Meta:
        model = IncidentHistory
        fields = [
            'id',
            'start_date',
            'end_date',
            'crisis_scenario_name',
            'risks_incident'
        ]


class ServicesUsedAffectedByIncidentSerializer(serializers.ModelSerializer):
    crisis_scenario_name = serializers.CharField(read_only=True, source="crisis_scenario.name")
    # Serializer aninado
    risks_incident = ServicesUsedRiskSerializer(many=True, read_only=True, source='crisis_scenario._risks')
    
    class Meta:
        model = IncidentHistory
        fields = [
            'id',
            'start_date',
            'end_date',
            'crisis_scenario_name',
            'risks_incident'
        ]


class OrganizationActivitiesAffectedByIncidentSerializer(serializers.ModelSerializer):
    crisis_scenario_name = serializers.CharField(read_only=True, source="crisis_scenario.name")
    # Serializer aninado
    risks_incident = OrganizationActivitiesRiskSerializer(many=True, read_only=True, source='crisis_scenario._risks')
    
    class Meta:
        model = IncidentHistory
        fields = [
            'id',
            'start_date',
            'end_date',
            'crisis_scenario_name',
            'risks_incident'
        ]
