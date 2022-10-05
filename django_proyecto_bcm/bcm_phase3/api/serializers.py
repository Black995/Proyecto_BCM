from bcm_phase3.models import IncidentHistory, ContingencyPlanBlock
from bcm_phase1.models import CrisisScenario
from rest_framework import serializers
from django.db.models import F, Q
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from bcm_phase1.api.serializers import (RiskSerializer, ServicesOfferedRiskSerializer, 
                                        ServicesUsedRiskSerializer, OrganizationActivitiesRiskSerializer)
from rest_framework_recursive.fields import RecursiveField



class IncidentHistoryListSerializer(serializers.ModelSerializer):
    crisis_scenario_name = serializers.CharField(read_only=True, source="crisis_scenario.name")
    crisis_scenario_frequency = serializers.CharField(read_only=True, source="crisis_scenario.frequency")
    crisis_scenario_frequency_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = IncidentHistory
        fields = [
            'id',
            'start_date',
            'end_date',
            'description',
            'crisis_scenario',
            'crisis_scenario_name',
            'crisis_scenario_frequency',
            'crisis_scenario_frequency_name'
        ]

    def get_crisis_scenario_frequency_name(self, obj):
        return dict(CrisisScenario.FREQUENCY).get(obj.crisis_scenario.frequency)


class IncidentHistorySerializer(serializers.ModelSerializer):
    crisis_scenario_name = serializers.CharField(read_only=True, source="crisis_scenario.name")
    crisis_scenario_description = serializers.CharField(read_only=True, source="crisis_scenario.description")
    crisis_scenario_frequency = serializers.CharField(read_only=True, source="crisis_scenario.frequency")
    crisis_scenario_frequency_name = serializers.CharField(read_only=True, source="crisis_scenario.frequency")
    
    class Meta:
        model = IncidentHistory
        fields = [
            'id',
            'start_date',
            'end_date',
            'description',
            'crisis_scenario',
            'crisis_scenario_name',
            'crisis_scenario_description',
            'crisis_scenario_frequency',
            'crisis_scenario_frequency_name'
        ]

    def get_crisis_scenario_frequency_name(self, obj):
        return dict(CrisisScenario.FREQUENCY).get(obj.crisis_scenario_frequency)


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


class ContingencyPlanBlockSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContingencyPlanBlock
        fields = [
            'id',
            'block_id',
            'parent_block_id',
            'title',
            'description',
        ]


class ContingencyPlanBlockCreateSerializer(serializers.ModelSerializer):
    contingency_plan_list = serializers.ListField(
        child=serializers.JSONField(), required=False)

    class Meta:
        model = CrisisScenario
        fields = [
            'id',
            'name',
            'description',
            'contingency_plan_list'
        ]


    def update(self, instance, validated_data):
        crisis_scenario = validated_data.get('crisis_scenario', instance)
        contingency_plan_list = validated_data.get('contingency_plan_list')
        
        """
            Si se envía el campo contingency_plan_list entonces se procede a crear los registros en 
            el modelo ContingencyPlanBlocks
        """
        # Primero se eliminan los registros anteriores asociados al escenario crítico
        ContingencyPlanBlock.objects.filter(crisis_scenario=instance.id).delete()

        contingency_block_plans = [
            ContingencyPlanBlock(
                block_id = e['block_id'],
                parent_block_id = e['parent_block_id'],
                title = e['title'],
                description = e['description'],
                crisis_scenario = crisis_scenario
            )
            for e in contingency_plan_list
        ]
        ContingencyPlanBlock.objects.bulk_create(contingency_block_plans)
        
        return instance

