from configuration.models import Area, Scale, ScaleView, Position
from rest_framework import serializers
from django.db.models import F, Q


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = [
            'id',
            'name'
        ]


class ScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scale
        fields = [
            'id',
            'name',
            'min_value',
            'max_value',
        ]

    def validate(self, attrs):
        min_value = attrs.get('min_value')
        max_value = attrs.get('max_value')

        if(max_value < min_value):
            raise serializers.ValidationError(
                'El valor máximo debe ser mayor al valor mínimo')
        elif(max_value == min_value):
            raise serializers.ValidationError(
                'Los valores mínimo y máximo no pueden ser iguales')
        else:
            return super().validate(attrs)


class ScaleViewSerializer(serializers.ModelSerializer):
    scale_name = serializers.CharField(read_only=True)
    scale_min_value = serializers.CharField(read_only=True)
    scale_max_value = serializers.CharField(read_only=True)

    class Meta:
        model = ScaleView
        fields = [
            'id',
            'name',
            'scale',
            'scale_name',
            'scale_min_value',
            'scale_max_value',
        ]


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = [
            'id',
            'name',
            'relevant'
        ]
