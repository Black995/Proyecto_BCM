from bcm_phase3.models import IncidentHistory, ContingencyPlanBlock
from bcm_phase1.models import CrisisScenario
from .serializers import (IncidentHistoryListSerializer, IncidentHistorySerializer,
                            ServicesOfferedAffectedByIncidentSerializer, RisksAffectedByIncidentSerializer,
                            ServicesUsedAffectedByIncidentSerializer, OrganizationActivitiesAffectedByIncidentSerializer,
                            ContingencyPlanBlockCreateSerializer, ContingencyPlanBlockSerializer)
from django.db.models import Q, F
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework import viewsets
from bcm_phase3.api.filters import (IncidentDatesFilterBackend, ContingencyPlanBlockByCrisisScenarioFilterBackend)


class IncidentHistoryListViewSet(viewsets.ModelViewSet):
    model = IncidentHistory
    queryset = IncidentHistory.objects.all().order_by('start_date')
    serializer_class = IncidentHistoryListSerializer
    filter_backends = [IncidentDatesFilterBackend, ]


class IncidentHistoryViewSet(viewsets.ModelViewSet):
    model = IncidentHistory
    queryset = IncidentHistory.objects.all().order_by('start_date')
    serializer_class = IncidentHistorySerializer 


class RisksAffectedByIncidentViewSet(viewsets.ModelViewSet):
    model = IncidentHistory
    queryset = IncidentHistory.objects.all()
    serializer_class = RisksAffectedByIncidentSerializer
    filter_backends = [IncidentDatesFilterBackend, ]


class ServicesOfferedAffectedByIncidentViewSet(viewsets.ModelViewSet):
    model = IncidentHistory
    queryset = IncidentHistory.objects.all()
    serializer_class = ServicesOfferedAffectedByIncidentSerializer
    filter_backends = [IncidentDatesFilterBackend, ]


class ServicesUsedAffectedByIncidentViewSet(viewsets.ModelViewSet):
    model = IncidentHistory
    queryset = IncidentHistory.objects.all()
    serializer_class = ServicesUsedAffectedByIncidentSerializer
    filter_backends = [IncidentDatesFilterBackend, ]


class OrganizationActivitiesAffectedByIncidentViewSet(viewsets.ModelViewSet):
    model = IncidentHistory
    queryset = IncidentHistory.objects.all()
    serializer_class = OrganizationActivitiesAffectedByIncidentSerializer 
    filter_backends = [IncidentDatesFilterBackend, ]


class ContingencyPlanBlockCreateViewSet(viewsets.ModelViewSet):
    model = CrisisScenario
    queryset = CrisisScenario.objects.all()
    serializer_class = ContingencyPlanBlockCreateSerializer

    
class ContingencyPlanBlockViewSet(viewsets.ModelViewSet):
    model = ContingencyPlanBlock
    queryset = ContingencyPlanBlock.objects.all().order_by('block_id')
    serializer_class = ContingencyPlanBlockSerializer
    filter_backends = [ContingencyPlanBlockByCrisisScenarioFilterBackend, ]

