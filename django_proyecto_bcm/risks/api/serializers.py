from layout.models import Risk, CrisisScenario
from rest_framework import serializers


class RiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risk
        fields = [
            'id',
            'name',
            'description',
        ]


class CrisisScenarioSerializer(serializers.ModelSerializer):
    # Serializer aninado
    #risks = RiskSerializer(many=True, read_only=True)
    risks = serializers.ListField(child=serializers.IntegerField(), required=False)

    class Meta:
        model = CrisisScenario
        fields = [
            'id',
            'name',
            'description',
            'risks',
            #'risks_create',
        ]

    def create(self, validate_data):
        risks_data = validate_data.pop('risks', None)
        crisisScenario = CrisisScenario.objects.create(**validate_data)
        if(risks_data):
            for risk_id in risks_data:
                risk = Risk.objects.filter(id=risk_id).first()
                if(risk is not None):
                    crisisScenario._risks.add(risk)
        return crisisScenario
