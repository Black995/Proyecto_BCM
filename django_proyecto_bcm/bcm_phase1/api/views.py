from bcm_phase1.models import Risk, CrisisScenario
from django.shortcuts import get_object_or_404
from .serializers import RiskSerializer, CrisisScenarioSerializer, CrisisScenarioListSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Q, F


class RiskViewSet(viewsets.ModelViewSet):
    model = Risk
    queryset = Risk.objects.all().order_by('name')
    serializer_class = RiskSerializer


class CrisisScenarioViewSet(viewsets.ModelViewSet):
    model = CrisisScenario
    queryset = CrisisScenario.objects.all()
    serializer_class = CrisisScenarioSerializer


class CrisisScenarioListViewSet(viewsets.ModelViewSet):
    model = CrisisScenario
    queryset = CrisisScenario.objects.all().order_by('name')
    serializer_class = CrisisScenarioListSerializer

class CrisisScenarioListRisksViewSet(viewsets.ModelViewSet):
    model = CrisisScenario
    queryset = CrisisScenario.objects.all()
    serializer_class = CrisisScenarioSerializer

