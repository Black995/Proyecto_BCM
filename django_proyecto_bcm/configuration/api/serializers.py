from configuration.models import Area, Scale, ScaleView, Position, Headquarter, State, City, Township, Parish, Organization
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
        

class HeadquarterSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(read_only=True, source="city.name")
    parish_name = serializers.CharField(read_only=True, source="parish.name")
    township_name = serializers.CharField(read_only=True, source="parish.township.name")
    state_name = serializers.CharField(read_only=True, source="parish.township.state.name")
    township = serializers.IntegerField(read_only=True, source="parish.township.id")
    state = serializers.IntegerField(read_only=True, source="parish.township.state.id")

    class Meta:
        model = Headquarter
        fields = [
            'id',
            'name',
            'city',
            'city_name',
            'parish',
            'parish_name',
            'township',
            'township_name',
            'state',
            'state_name',
        ]



"""
    Serializers de estados, ciudades, municipios y parroquias
"""
class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = [
            'id',
            'name',
            'iso_3166_2'
        ]


class CitySerializer(serializers.ModelSerializer):
    capital_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = City
        fields = [
            'id',
            'name',
            'capital',
            'capital_name',
            'state'
        ]
    
    def get_capital_name(self, obj):
        return dict(City.TYPE).get(obj.capital)


class TownshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Township
        fields = [
            'id',
            'name',
        ]


class ParishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parish
        fields = [
            'id',
            'name',
        ]


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            'id',
            'name',
            'legal_id',
            'description',
            'logo',
        ]
