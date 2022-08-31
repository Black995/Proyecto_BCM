from bcm_phase3.models import IncidentHistory, ContingencyPlan
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
            'crisis_scenario_frequency',
            'crisis_scenario_frequency_name'
        ]

    def get_crisis_scenario_frequency_name(self, obj):
        return dict(CrisisScenario.FREQUENCY).get(obj.crisis_scenario_frequency)


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


class ContingencyPlanSerializer(serializers.ModelSerializer):
    #contingency_father = serializers.SerializerMethodField()
    contingency_children = serializers.ListField(child=RecursiveField())

    class Meta:
        model = ContingencyPlan
        fields = [
            'id',
            'number_order',
            'description',
            'contingency_children'
        ]


class ContingencyPlanCreateSerializer(serializers.ModelSerializer):
    contingency_plan_list = serializers.ListField(
        child=serializers.JSONField(), required=False)

    class Meta:
        model = ContingencyPlan
        fields = [
            'id',
            'number_order',
            'description',
            'crisis_scenario',
            'contingency_plan_list'
        ]


    def update(self, instance, validated_data):
        crisis_scenario = validated_data.get('crisis_scenario', instance.crisis_scenario)
        contingency_plan_list = validated_data.get('contingency_plan_list')
        
        """
            Si se envía el campo contingency_plan entonces se procede a crear los registros en 
            el modelo ContingencyPlan
        """
        print('Escenario crítico')
        print(crisis_scenario)
        print('Plan de contingencia')
        print(contingency_plan_list)
        """
        if staffs_json is not None:
            SO_S.objects.filter(service_offered=service).delete()

            for s in staffs_json:
                staff = Staff.objects.get(id=s['staff'])

                SO_S.objects.create(
                    relevant=s['relevant'],
                    service_offered=service,
                    staff=staff
                )
        """
                
        instance.save()
        return instance

