from bcm_phase2.models import InterestedParty, ServiceOffered, ServiceUsed, Staff, OrganizationActivity
from django.shortcuts import get_object_or_404
from .serializers import InterestedPartyListSerializer, OrganizationActivityListSerializer, OrganizationActivitySerializer, ServiceOfferedListSerializer, ServiceOfferedSerializer, ServiceUsedListSerializer, ServiceUsedSerializer, StaffListSerializer, StaffSerializer, interestedPartySerializer
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
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

class OrganizationActivityListViewSet(viewsets.ModelViewSet):
    model = OrganizationActivity
    queryset = OrganizationActivity.objects.annotate(
        scale_max_value=F('scale__max_value')).order_by('name')
    serializer_class = OrganizationActivityListSerializer

class OrganizationActivityViewSet(viewsets.ModelViewSet):
    model = OrganizationActivity
    queryset = OrganizationActivity.objects.annotate(scale_name=F('scale__name'), scale_min_value=F(
        'scale__min_value'), scale_max_value=F('scale__max_value'))

    serializer_class = OrganizationActivitySerializer


class InterestedPartyListViewSet(viewsets.ModelViewSet):
    model = InterestedParty
    queryset = InterestedParty.objects.all().order_by('name')
    serializer_class = InterestedPartyListSerializer


class InterestedPartyViewSet(viewsets.ModelViewSet):
    model = InterestedParty
    queryset = InterestedParty.objects.annotate(organization_name=F('organization__name'))
    serializer_class = interestedPartySerializer