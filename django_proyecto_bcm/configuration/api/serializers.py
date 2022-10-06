from datetime import timedelta
from configuration.models import Area, Scale, ScaleView, Position, Headquarter, State, City, Township, Parish, Organization, ProductActivation,UsedKeys
from rest_framework import serializers
from django.db.models import F, Q
from django.utils import timezone
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


import binascii
import Crypto
import base64
import os
from django.conf import settings

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
    scale_name = serializers.CharField(read_only=True, source="scale.name")
    scale_min_value = serializers.CharField(read_only=True, source="scale.min_value")
    scale_max_value = serializers.CharField(read_only=True, source="scale.max_value")

    class Meta:
        model = ScaleView
        fields = [
            'id',
            'name',
            'scale',
            'scale_name',
            'scale_min_value',
            'scale_max_value',
            'minimum_recovery_time',
            'minimum_scale_value'
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
    logo_base64 = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Organization
        fields = [
            'id',
            'name',
            'legal_id',
            'description',
            'logo',
            'logo_base64'
        ]

    def get_logo_base64(self, obj):
        path = str(Organization.objects.get(id=obj.id).logo)
        file_path = os.path.join(settings.STATICFILES_DIRS[0], path)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                return base64.b64encode(fh.read()).decode('utf-8')
        return None

class ProductActivationListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductActivation
        fields = [
            'id',
            'state',
            'activation_date'
        ]

class UsedKeysSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsedKeys
        fields = [
            'id',
            'key'
        ]

    def validate(self, attrs):
        key = attrs.get('key')
        keys = UsedKeys.objects.filter(key=key)

        if(keys):
            raise serializers.ValidationError(
                'Esta llave ya fue usada. Ingrese una llave válida.')
        else: 
            return super().validate(attrs)

    
    def create(self, validated_data):
        private_key = '3082025b02010002818100c7e9c4906fb3ae64496751e139cc15e859dc258cf29a7fd32d1d4c93c7a643cd8ed2878c224f3607b1332665d995fd4a0ea778d1b44af685c9dd7d94583eb25819ff38ef369042087ff6171b8ff7ba9eaf0646609b5149d2ea5da1e107d49c0d9d5f26ebf4c020445d6341698ee8adff8234d702c457c2f85b7c5a7609f37d03020301000102818049959f77b6d6019c0274d86bb9b5885ed52cb659b236f2540de819f6cf6740cfda015e49539baa7c9c5a02893cd4fbbd95b549408f4784846c706db7fbdf600f6c72a7879a9a1599cd84a8389fe68b4e7eb6f7b0269ff87b54a8dbe1a54d6a09fe72a3f6fe7595d41fb3fb866ae7855053095967ffb81db79ddbac0c5c2754f9024100cd196dd9fa30b6f20a611311faefddb8c3bd79b5aa364f87a325902509f9b70cbc32cdd27ebcfe153c080aed9f915f64719e821ac7cb9141a3c8f3559cda512f024100f986d870e9f629468ad2afbdb96b1e092ef6ee9d7b6cae36205d8e84ce4a49bb19435471cdbf980c1282332df0d3d190193d5d3e66a5e1c37fd03f7d4d7cd46d02404ae94bcf3eeb861697a5e7323d0659647fd1f7df5b8124c134dca66e70db4d79904fba0f750d107caf057d0057b4e033aeb0277322a07eb88bdafccdbb519e2f02407a7e03ca8a4fd93b53f2d16ae596fc0bae0e725cc4b6395f40cc2ca66d4e729b726f6708e6e3e3142a11d865f90f4294e68f053318d8ddd746eb47ff8f06749102404c72eca322eea0e1e996fee011ecf1d1f7e2842bc3bbe07eef8000f31282c3ba76c2f420f9e157d64eb0554c7315183ddbb7b2c15a8e3923150e5bb464705735'
        
        private_key = RSA.importKey(binascii.unhexlify(private_key))
        
        cipher = PKCS1_OAEP.new(private_key)
        key1 = validated_data.get('key')

        key_byte = str.encode(key1)
        kbyte = key_byte.decode('unicode-escape').encode('ISO-8859-1') 


        key2 = cipher.decrypt(kbyte)
        keyStr = key2.decode("utf-8")
        print(type(keyStr))
        
        activated = ProductActivation.objects.all()
        if activated:
            for a in activated:
                if (a):
                    new_date = a.activation_date + timedelta(weeks=52)
                    a.activation_date = new_date
                    a.save()
                    keySaved = UsedKeys.objects.create(key=key1)
                else:
                    activated = ProductActivation.objects.create(state=True,activation_date=timezone.now().date() )
        else:
            activated = ProductActivation.objects.create(state=True,activation_date=timezone.now().date() )
            keySaved = UsedKeys.objects.create(key=key1)
        return keySaved