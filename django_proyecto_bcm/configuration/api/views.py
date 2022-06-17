from configuration.models import Area, Scale, ScaleView, Position, Headquarter
from django.shortcuts import get_object_or_404
from .serializers import AreaSerializer, ScaleSerializer, ScaleViewSerializer, PositionSerializer, HeadquarterSerializer
from rest_framework import viewsets
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


class PositionViewSet(viewsets.ModelViewSet):
    model = Position
    queryset = Position.objects.all().order_by('name')
    serializer_class = PositionSerializer


class HeadquarterViewSet(viewsets.ModelViewSet):
    model = Headquarter
    queryset = Headquarter.objects.annotate(location_name=F('location__name')).order_by('name')
    serializer_class = HeadquarterSerializer