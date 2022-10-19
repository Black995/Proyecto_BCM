from asyncio.windows_events import NULL
from re import L
from configuration.models import Area, ProductActivation, Scale, ScaleView, Position, Headquarter, State, City, Township, Parish, Organization, UsedKeys,PrivatePublicKey
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
        if(option == '1'):
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
        
        pr_key = PrivatePublicKey.objects.all()


        private_key = pr_key[0].key

        print(private_key)
        
        private_key = RSA.importKey(binascii.unhexlify(private_key))
        
        cipher = PKCS1_OAEP.new(private_key)
        

        file = validated_data.data.get('licencia')
        #file1 = open(file,'r')
        line1 = NULL
        for l in file:
            line1 = l
        
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
