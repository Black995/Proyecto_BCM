from bcm_phase1.models import Risk, CrisisScenario
from rest_framework import serializers
from django.db.models import F, Q


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


"""
    def create(self, validate_data):
        risks_data = validate_data.pop('risks', None)
        crisisScenario = CrisisScenario.objects.create(**validate_data)
        if(risks_data):
            for risk_id in risks_data:
                risk = Risk.objects.filter(id=risk_id).first()
                if(risk is not None):
                    crisisScenario._risks.add(risk)
        return crisisScenario
"""


class CrisisScenarioListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CrisisScenario
        fields = [
            'id',
            'name',
            'description',
        ]
