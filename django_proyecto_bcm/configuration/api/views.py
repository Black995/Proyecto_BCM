from configuration.models import Area, Scale, ScaleView
from django.shortcuts import get_object_or_404
from .serializers import AreaSerializer, ScaleSerializer, ScaleViewSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Q, F


class AreaViewSet(viewsets.ModelViewSet):
    model = Area
    queryset = Area.objects.all()
    serializer_class = AreaSerializer


class ScaleViewSet(viewsets.ModelViewSet):
    model = Scale
    queryset = Scale.objects.all()
    serializer_class = ScaleSerializer


class ScaleviewViewSet(viewsets.ModelViewSet):
    model = ScaleView
    queryset = ScaleView.objects.annotate(scale_name=F('scale__name'))
    serializer_class = ScaleViewSerializer
