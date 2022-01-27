from bcm_phase2.models import ServiceOffered
from django.shortcuts import get_object_or_404
from .serializers import ServiceOfferedSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Q, F


class ServiceOfferedViewSet(viewsets.ModelViewSet):
    model = ServiceOffered
    queryset = ServiceOffered.objects.annotate(area_name=F('area__name'))
    serializer_class = ServiceOfferedSerializer