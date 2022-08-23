from bcm_phase3.models import IncidentHistory, ContingencyPlan
from .serializers import (IncidentHistoryListSerializer, IncidentHistorySerializer,
                            ServicesOfferedAffectedByIncidentSerializer, RisksAffectedByIncidentSerializer,
                            ServicesUsedAffectedByIncidentSerializer, OrganizationActivitiesAffectedByIncidentSerializer,
                            ContingencyPlanCreateSerializer, ContingencyPlanSerializer)
from django.db.models import Q, F
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework import viewsets
from bcm_phase3.api.filters import (IncidentDatesFilterBackend, ContingencyPlanByCrisisScenarioFilterBackend)


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


class ContingencyPlanCreateViewSet(viewsets.ModelViewSet):
    model = ContingencyPlan
    queryset = ContingencyPlan.objects.all()
    serializer_class = ContingencyPlanCreateSerializer

    
class ContingencyPlanViewSet(viewsets.ModelViewSet):
    model = ContingencyPlan
    queryset = ContingencyPlan.objects.filter(contingency_children__isnull=True).order_by('number_order')
    serializer_class = ContingencyPlanSerializer
    filter_backends = [ContingencyPlanByCrisisScenarioFilterBackend, ]

