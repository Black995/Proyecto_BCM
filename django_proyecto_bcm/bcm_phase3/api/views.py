from bcm_phase3.models import IncidentHistory
from .serializers import (IncidentHistoryListSerializer, IncidentHistorySerializer,
                            ServicesOfferedAffectedByIncidentSerializer, RisksAffectedByIncidentSerializer,
                            ServicesUsedAffectedByIncidentSerializer, OrganizationActivitiesAffectedByIncidentSerializer,
                            )
from django.db.models import Q, F
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework import viewsets
from bcm_phase3.api.filters import (IncidentDatesFilterBackend)


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


class ServicesOfferedAffectedByIncidentViewSet(viewsets.ModelViewSet):
    model = IncidentHistory
    queryset = IncidentHistory.objects.all()
    serializer_class = ServicesOfferedAffectedByIncidentSerializer 


class ServicesUsedAffectedByIncidentViewSet(viewsets.ModelViewSet):
    model = IncidentHistory
    queryset = IncidentHistory.objects.all()
    serializer_class = ServicesUsedAffectedByIncidentSerializer 


class OrganizationActivitiesAffectedByIncidentViewSet(viewsets.ModelViewSet):
    model = IncidentHistory
    queryset = IncidentHistory.objects.all()
    serializer_class = OrganizationActivitiesAffectedByIncidentSerializer 

