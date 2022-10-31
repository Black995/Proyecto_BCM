import csv
import os
from django.conf import settings
from bcm_phase2.models import (R_SO, InterestedParty, Ressource, ServiceOffered, ServiceUsed, Staff, 
                                OrganizationActivity, SO_S)
from django.shortcuts import get_object_or_404
from .serializers import (InterestedPartyListSerializer, OrganizationActivityListSerializer, OrganizationActivitySerializer, R_SOSerializer, RessourceListSerializer, RessourceSerializer, RessourceWithServiceOfferedSerializer, 
                            ServiceOfferedListSerializer, ServiceOfferedSerializer, ServiceUsedListSerializer, 
                            ServiceUsedSerializer, StaffListSerializer, StaffSerializer, interestedPartySerializer,
                            SO_SSerializer, ServiceOfferedWithStaffsSerializer)
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q, F
from bcm_phase2.api.filters import (R_SOFilterBackend, SO_SFilterBackend)
from rest_framework.generics import (ListAPIView)
from django.http.response import Http404
from django.shortcuts import HttpResponse
from .utils import render_to_pdf


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

    

class download_excel_massive_load_staff(ListAPIView):
    queryset = Staff.objects.all()

    def get(self, request):
        file_path = os.path.join(
            settings.STATICFILES_DIRS[2], 'massive_load_staff.xlsx')
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(
                    fh.read(), content_type="application/vnd.ms-Excel")
                response['Content-Disposition'] = 'inline; filename=' + \
                    os.path.basename(file_path)
                return response
        raise Http404

class RessourceListViewSet(viewsets.ModelViewSet):
    model = Ressource
    queryset = Ressource.objects.all().order_by('name')
    serializer_class = RessourceListSerializer

class RessourceViewSet(viewsets.ModelViewSet):
    model = Ressource
    queryset = Ressource.objects.all()
    serializer_class = RessourceSerializer 

class R_SOViewSet(viewsets.ModelViewSet):
    model = R_SO
    queryset = R_SO.objects.all()
    serializer_class = R_SOSerializer
    filter_backends = [R_SOFilterBackend]

class RessourceWithServiceOfferedViewSet(viewsets.ModelViewSet):
    model = Ressource
    queryset = Ressource.objects.all()
    serializer_class = RessourceWithServiceOfferedSerializer


class GenerateServiceOffered(APIView):
    queryset = ServiceOffered.objects.all()

    def get(self,request,*args,**kwargs):
        services = ServiceOffered.objects.all()
        serviceOffered = []
        print(1)
        for s in services:
            serviceOffered.append({
                "name": s.name,
                "type": dict(ServiceOffered.TYPE).get(s.type),
                "area": s.area.name,
                "criticality": s.criticality,
                "max_scale": s.scale.max_value,
                "rto":s.maximum_recovery_time
            })
        
        data = {
            "serviceOffered": serviceOffered
        }

        pdf = render_to_pdf("service_offered.html",data)
        return HttpResponse(pdf,content_type='application/pdf')