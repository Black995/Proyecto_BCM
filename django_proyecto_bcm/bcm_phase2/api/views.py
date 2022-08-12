from bcm_phase2.models import (InterestedParty, ServiceOffered, ServiceUsed, Staff, 
                                OrganizationActivity, SO_S)
from django.shortcuts import get_object_or_404
from .serializers import (InterestedPartyListSerializer, OrganizationActivityListSerializer, OrganizationActivitySerializer, 
                            ServiceOfferedListSerializer, ServiceOfferedSerializer, ServiceUsedListSerializer, 
                            ServiceUsedSerializer, StaffListSerializer, StaffSerializer, interestedPartySerializer,
                            SO_SSerializer, ServiceOfferedWithStaffsSerializer)
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Q, F
from bcm_phase2.api.filters import (SO_SFilterBackend)


class ServiceOfferedListViewSet(viewsets.ModelViewSet):
    model = ServiceOffered
    queryset = ServiceOffered.objects.all().order_by('name')
    serializer_class = ServiceOfferedListSerializer


class ServiceOfferedViewSet(viewsets.ModelViewSet):
    model = ServiceOffered
    queryset = ServiceOffered.objects.all()
    serializer_class = ServiceOfferedSerializer


class ServiceOfferedWithStaffsViewSet(viewsets.ModelViewSet):
    model = ServiceOffered
    queryset = ServiceOffered.objects.all()
    serializer_class = ServiceOfferedWithStaffsSerializer



class ServiceUsedListViewSet(viewsets.ModelViewSet):
    model = ServiceUsed
    queryset = ServiceUsed.objects.all().order_by('name')
    serializer_class = ServiceUsedListSerializer


class ServiceUsedViewSet(viewsets.ModelViewSet):
    model = ServiceUsed
    queryset = ServiceUsed.objects.all()
    serializer_class = ServiceUsedSerializer


class StaffListViewSet(viewsets.ModelViewSet):
    model = Staff
    queryset = Staff.objects.all().order_by('staff_number')
    serializer_class = StaffListSerializer


class StaffViewSet(viewsets.ModelViewSet):
    model = Staff
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

class OrganizationActivityListViewSet(viewsets.ModelViewSet):
    model = OrganizationActivity
    queryset = OrganizationActivity.objects.all().order_by('name')
    serializer_class = OrganizationActivityListSerializer

class OrganizationActivityViewSet(viewsets.ModelViewSet):
    model = OrganizationActivity
    queryset = OrganizationActivity.objects.all()

    serializer_class = OrganizationActivitySerializer


class InterestedPartyListViewSet(viewsets.ModelViewSet):
    model = InterestedParty
    queryset = InterestedParty.objects.all().order_by('name')
    serializer_class = InterestedPartyListSerializer


class InterestedPartyViewSet(viewsets.ModelViewSet):
    model = InterestedParty
    queryset = InterestedParty.objects.all()
    serializer_class = interestedPartySerializer


class SO_SViewSet(viewsets.ModelViewSet):
    model = SO_S
    queryset = SO_S.objects.all()
    serializer_class = SO_SSerializer
    filter_backends = [SO_SFilterBackend, ]

    