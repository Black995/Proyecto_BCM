from layout.models import Risk
from rest_framework import serializers


class RiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risk
        fields = [
            "id",
            'name',
            'description',
        ]
