import os
from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import HttpResponse, get_object_or_404
from configuration.models import Area, Scale, ScaleView, Position, Headquarter, State, City, Township, Parish, Organization
from bcm_phase2.models import ServiceOffered, ServiceUsed, OrganizationActivity
from django.shortcuts import get_object_or_404
from .serializers import AreaSerializer, ScaleSerializer, ScaleViewSerializer, PositionSerializer, HeadquarterSerializer, StateSerializer, CitySerializer, TownshipSerializer, ParishSerializer, OrganizationSerializer
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from django.db.models import Q, F
from configuration.api.filters import (ScaleViewFilterBackend, CityTownshipFilterBackend, ParishFilterBackend)
from rest_framework.views import APIView


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
    queryset = ScaleView.objects.annotate(scale_name=F('scale__name'), scale_min_value=F(
        'scale__min_value'), scale_max_value=F('scale__max_value')).order_by('name')
    serializer_class = ScaleViewSerializer
    filter_backends = [ScaleViewFilterBackend, ]

    # Al actualizar la escala se debe tener la opción de:
    # 1. Pasar a nulo todas las escalas de todos los ServiceOffered, ServiceUsed y OrganizationActivity
    # 2. Hacer un promedio de las escalas existentes    
    def partial_update(self, request, pk):
        name = request.data.get('name')
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

        updated = ScaleView.objects.filter(name=name).update(scale=new_scale)
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


