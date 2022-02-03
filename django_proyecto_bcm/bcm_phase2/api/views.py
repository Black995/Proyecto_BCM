from bcm_phase2.models import ServiceOffered
from django.shortcuts import get_object_or_404
from .serializers import ServiceOfferedListSerializer, ServiceOfferedSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Q, F


class ServiceOfferedListViewSet(viewsets.ModelViewSet):
    model = ServiceOffered
    queryset = ServiceOffered.objects.annotate(area_name=F(
        'area__name'), scale_max_value=F('scale__max_value'))
    serializer_class = ServiceOfferedSerializer


class ServiceOfferedViewSet(viewsets.ModelViewSet):
    model = ServiceOffered
    queryset = ServiceOffered.objects.annotate(area_name=F('area__name'), scale_name=F('scale__name'), scale_min_value=F(
        'scale__min_value'), scale_max_value=F('scale__max_value'))
    serializer_class = ServiceOfferedSerializer
