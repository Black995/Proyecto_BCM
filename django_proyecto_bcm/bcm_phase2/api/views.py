from bcm_phase2.models import ServiceOffered, ServiceUsed, Staff
from django.shortcuts import get_object_or_404
from .serializers import ServiceOfferedListSerializer, ServiceOfferedSerializer, ServiceUsedListSerializer, ServiceUsedSerializer, StaffListSerializer, StaffSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Q, F


class ServiceOfferedListViewSet(viewsets.ModelViewSet):
    model = ServiceOffered
    queryset = ServiceOffered.objects.annotate(area_name=F(
        'area__name'), scale_max_value=F('scale__max_value')).order_by('name')
    serializer_class = ServiceOfferedListSerializer


class ServiceOfferedViewSet(viewsets.ModelViewSet):
    model = ServiceOffered
    queryset = ServiceOffered.objects.annotate(area_name=F('area__name'), scale_name=F('scale__name'), scale_min_value=F(
        'scale__min_value'), scale_max_value=F('scale__max_value'))
    serializer_class = ServiceOfferedSerializer


class ServiceUsedListViewSet(viewsets.ModelViewSet):
    model = ServiceUsed
    queryset = ServiceUsed.objects.annotate(
        scale_max_value=F('scale__max_value')).order_by('name')
    serializer_class = ServiceUsedListSerializer


class ServiceUsedViewSet(viewsets.ModelViewSet):
    model = ServiceUsed
    queryset = ServiceUsed.objects.annotate(scale_name=F('scale__name'), scale_min_value=F(
        'scale__min_value'), scale_max_value=F('scale__max_value'))
    serializer_class = ServiceUsedSerializer


class StaffListViewSet(viewsets.ModelViewSet):
    model = Staff
    queryset = Staff.objects.annotate(area_name=F('area__name'), 
        position_name=F('position__name')).order_by('staff_number')
    serializer_class = StaffListSerializer


class StaffViewSet(viewsets.ModelViewSet):
    model = Staff
    queryset = Staff.objects.annotate(user_email=F('user__email'))
    serializer_class = StaffSerializer

