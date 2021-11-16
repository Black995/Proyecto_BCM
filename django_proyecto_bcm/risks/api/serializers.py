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
    risks = RiskSerializer(many=True)

    class Meta:
        model = CrisisScenario
        fields = [
            'id',
            'name',
            'description',
            'risks'
        ]

    def create(self, validate_data):
        risks_data = validate_data.pop('risks')
        print()
        print('OBTENIENDO DATOS DE OS RIESGOS')
        print(risks_data)
        crisisScenario = CrisisScenario.objects.create(**validate_data)
        for risk_id in risks_data:
            print(risk_id)
            risk = Risk.objects.get(id=risk_id)
            crisisScenario.risks.add(risk)
            # Risk.objects.create(crisisScenario=crisisScenario, **risks_data)
        return crisisScenario
