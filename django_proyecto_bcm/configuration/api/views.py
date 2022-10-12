from asyncio.windows_events import NULL
from re import L
from configuration.models import Area, ProductActivation, Scale, ScaleView, Position, Headquarter, State, City, Township, Parish, Organization, UsedKeys
from bcm_phase2.models import ServiceOffered, ServiceUsed, OrganizationActivity
from django.shortcuts import get_object_or_404
from .serializers import AreaSerializer, ProductActivationListSerializer, ScaleSerializer, ScaleViewSerializer, PositionSerializer, HeadquarterSerializer, StateSerializer, CitySerializer, TownshipSerializer, ParishSerializer, OrganizationSerializer
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from django.db.models import Q, F
from configuration.api.filters import (ScaleViewFilterBackend, CityTownshipFilterBackend, ParishFilterBackend)
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.utils import timezone
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from datetime import datetime, timedelta


import urllib3
import binascii
import Crypto
import io

class AreaViewSet(viewsets.ModelViewSet):
    model = Area
    queryset = Area.objects.all().order_by('name')
    serializer_class = AreaSerializer


class ScaleViewSet(viewsets.ModelViewSet):
    model = Scale
    queryset = Scale.objects.all().order_by('name')
    serializer_class = ScaleSerializer


class ScaleviewViewSet(viewsets.ModelViewSet):
    model = ScaleView
    queryset = ScaleView.objects.all().order_by('name')
    serializer_class = ScaleViewSerializer
    filter_backends = [ScaleViewFilterBackend, ]

    # Al actualizar la escala se debe tener la opción de:
    # 1. Pasar a nulo todas las escalas de todos los ServiceOffered, ServiceUsed y OrganizationActivity
    # 2. Hacer un promedio de las escalas existentes    
    def partial_update(self, request, pk):
        name = request.data.get('name')
        minimum_recovery_time = request.data.get('minimum_recovery_time')
        minimum_scale_value = request.data.get('minimum_scale_value')
        scale_id = request.data.get('scale')
        option = request.data.get('option')
        new_scale = Scale.objects.get(id=scale_id)
        print(option)
        if(option == '1'):
            print('opción 1')
            if(name == 'Servicios de la Organización'):
                ServiceOffered.objects.filter(criticality__isnull=False).update(criticality=None, scale=None)
            elif(name == 'Servicios de Soporte'):
                ServiceUsed.objects.filter(criticality__isnull=False).update(criticality=None, scale=None)
            if(name == 'Actividades de la Organización'):
                OrganizationActivity.objects.filter(criticality__isnull=False).update(criticality=None, scale=None)
        elif(option == '2'):
            if(name == 'Servicios de la Organización'):
                list_obj = ServiceOffered.objects.filter(criticality__isnull=False, scale__isnull=False)
            elif(name == 'Servicios de Soporte'):
                list_obj = ServiceUsed.objects.filter(criticality__isnull=False, scale__isnull=False)
            elif(name == 'Actividades de la Organización'):
                list_obj = OrganizationActivity.objects.filter(criticality__isnull=False, scale__isnull=False)
            else: 
                list_obj = []
            for s in list_obj:
                    new_value = round(s.criticality*new_scale.max_value/s.scale.max_value)
                    s.criticality= new_value if(new_value>=new_scale.min_value) else new_scale.min_value
                    s.scale=new_scale
                    s.save()
        else:
            raise serializers.ValidationError(
                {'Error': 'Opción seleccionada inválida'})

        updated = ScaleView.objects.filter(name=name).update(scale=new_scale, minimum_recovery_time=minimum_recovery_time, minimum_scale_value=minimum_scale_value)
        msg, sta = ('Escalas actualizadas exitosamente', status.HTTP_200_OK) if updated else (
            'Las escalas no pudieron ser actualizadas', status.HTTP_400_BAD_REQUEST)
        return Response({'Error': msg}, status=sta)



class PositionViewSet(viewsets.ModelViewSet):
    model = Position
    queryset = Position.objects.all().order_by('name')
    serializer_class = PositionSerializer


class HeadquarterViewSet(viewsets.ModelViewSet):
    model = Headquarter
    queryset = Headquarter.objects.order_by('name')
    serializer_class = HeadquarterSerializer


"""
    Vistas de estados, ciudades, municipios y parroquias
"""
class StateViewSet(viewsets.ModelViewSet):
    model = State
    queryset = State.objects.order_by('name')
    serializer_class = StateSerializer


class CityViewSet(viewsets.ModelViewSet):
    model = City
    queryset = City.objects.order_by('name')
    serializer_class = CitySerializer
    filter_backends = [CityTownshipFilterBackend, ]


class TownshipViewSet(viewsets.ModelViewSet):
    model = Township
    queryset = Township.objects.order_by('name')
    serializer_class = TownshipSerializer
    filter_backends = [CityTownshipFilterBackend, ]


class ParishViewSet(viewsets.ModelViewSet):
    model = Parish
    queryset = Parish.objects.order_by('name')
    serializer_class = ParishSerializer
    filter_backends = [ParishFilterBackend, ]


class OrganizationViewSet(viewsets.ModelViewSet):
    model = Organization
    queryset = Organization.objects.order_by('name')
    serializer_class = OrganizationSerializer


class ProductActivatationListViewSet(viewsets.ModelViewSet):
    model = ProductActivation
    queryset = ProductActivation.objects.all()
    serializer_class = ProductActivationListSerializer

class UsedKeysViewSet(viewsets.ModelViewSet):
    model = UsedKeys
    queryset = UsedKeys.objects.all()
    http_method_names = ['post']
    permission_classes=[AllowAny]

    def create(self, validated_data):
        
        http = urllib3.PoolManager()
        res = http.request('GET','http://just-the-time.appspot.com/')
        
        result = res.data

        date_str = result.decode('utf-8')

        dateL = date_str.split(" ")

        date = datetime.strptime(dateL[0], '%Y-%m-%d').date()
        

        private_key = '3082025b02010002818100c7e9c4906fb3ae64496751e139cc15e859dc258cf29a7fd32d1d4c93c7a643cd8ed2878c224f3607b1332665d995fd4a0ea778d1b44af685c9dd7d94583eb25819ff38ef369042087ff6171b8ff7ba9eaf0646609b5149d2ea5da1e107d49c0d9d5f26ebf4c020445d6341698ee8adff8234d702c457c2f85b7c5a7609f37d03020301000102818049959f77b6d6019c0274d86bb9b5885ed52cb659b236f2540de819f6cf6740cfda015e49539baa7c9c5a02893cd4fbbd95b549408f4784846c706db7fbdf600f6c72a7879a9a1599cd84a8389fe68b4e7eb6f7b0269ff87b54a8dbe1a54d6a09fe72a3f6fe7595d41fb3fb866ae7855053095967ffb81db79ddbac0c5c2754f9024100cd196dd9fa30b6f20a611311faefddb8c3bd79b5aa364f87a325902509f9b70cbc32cdd27ebcfe153c080aed9f915f64719e821ac7cb9141a3c8f3559cda512f024100f986d870e9f629468ad2afbdb96b1e092ef6ee9d7b6cae36205d8e84ce4a49bb19435471cdbf980c1282332df0d3d190193d5d3e66a5e1c37fd03f7d4d7cd46d02404ae94bcf3eeb861697a5e7323d0659647fd1f7df5b8124c134dca66e70db4d79904fba0f750d107caf057d0057b4e033aeb0277322a07eb88bdafccdbb519e2f02407a7e03ca8a4fd93b53f2d16ae596fc0bae0e725cc4b6395f40cc2ca66d4e729b726f6708e6e3e3142a11d865f90f4294e68f053318d8ddd746eb47ff8f06749102404c72eca322eea0e1e996fee011ecf1d1f7e2842bc3bbe07eef8000f31282c3ba76c2f420f9e157d64eb0554c7315183ddbb7b2c15a8e3923150e5bb464705735'
        
        private_key = RSA.importKey(binascii.unhexlify(private_key))
        
        cipher = PKCS1_OAEP.new(private_key)
        

        file = validated_data.data.get('licencia')
        #file1 = open(file,'r')
        line = NULL
        line1 = NULL
        for l in file:
            line1 = l
            line = l.decode('unicode-escape').encode('ISO-8859-1')


            
        #lines = file1.readlines()
        
    
        
        key1 = line1.decode("utf-8")
        kbyte = line1.decode("utf-8").replace("b'","")
        kbyte = kbyte.replace("'","")
        kbyte = bytes(kbyte,"utf-8").decode('unicode-escape').encode('ISO-8859-1')
        key2 = cipher.decrypt(kbyte)
        key_validate = key2.decode("utf-8")
        keys = UsedKeys.objects.get(key=key1)
        if (keys):
            return Response(data={"Error": "La llave ya fue usada anteriormente"},status=400)
        if ( 1507 <= sum(ord(ch) for ch in key_validate) <= 1607) and (('P' in key_validate or 'p' in key_validate) or ('W' in key_validate or 'W' in key_validate) or ('C' in key_validate or 'c' in key_validate))  :
            activated = ProductActivation.objects.all()
            if activated:
                for a in activated:
                    if (a):
                        keySaved = UsedKeys.objects.create(key=key1)
                        new_date = a.activation_date + timedelta(weeks=52)
                        a.activation_date = new_date
                        a.save()

                    else:
                        keySaved = UsedKeys.objects.create(key=key1)
                        activated = ProductActivation.objects.create(state=True,activation_date=date)
            else:
                keySaved = UsedKeys.objects.create(key=key1)
                activated = ProductActivation.objects.create(state=True,activation_date=date )
            
            return Response(1)
        else:
            return Response(data={"Error":"La llave es invalida"}, status=400)
