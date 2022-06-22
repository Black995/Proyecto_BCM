from configuration.models import Area, Scale, ScaleView, Position, Headquarter
from bcm_phase2.models import ServiceOffered, ServiceUsed, OrganizationActivity
from django.shortcuts import get_object_or_404
from .serializers import AreaSerializer, ScaleSerializer, ScaleViewSerializer, PositionSerializer, HeadquarterSerializer
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from django.db.models import Q, F
from configuration.api.filters import (ScaleViewFilterBackend,)


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
        scale = request.data.get('scale')
        option = request.data.get('option')
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
            print('opción 2')
        else:
            raise serializers.ValidationError(
                {'Error': 'Opción seleccionada inválida'})

        updated = ScaleView.objects.filter(name=name).update(scale=Scale.objects.get(id=scale))
        msg, sta = ('Escalas actualizadas exitosamente', status.HTTP_200_OK) if updated else (
            'Las escalas no pudieron ser actualizadas', status.HTTP_400_BAD_REQUEST)
        return Response({'Error': msg}, status=sta)



class PositionViewSet(viewsets.ModelViewSet):
    model = Position
    queryset = Position.objects.all().order_by('name')
    serializer_class = PositionSerializer


class HeadquarterViewSet(viewsets.ModelViewSet):
    model = Headquarter
    queryset = Headquarter.objects.annotate(location_name=F('location__name')).order_by('name')
    serializer_class = HeadquarterSerializer