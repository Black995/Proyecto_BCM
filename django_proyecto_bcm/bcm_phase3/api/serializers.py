from bcm_phase3.models import IncidentHistory
from bcm_phase1.models import CrisisScenario
from rest_framework import serializers
from django.db.models import F, Q
from django.core.exceptions import ValidationError



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


    