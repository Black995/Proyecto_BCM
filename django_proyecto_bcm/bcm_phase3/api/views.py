from bcm_phase3.models import IncidentHistory
from .serializers import (IncidentHistoryListSerializer, IncidentHistorySerializer,
                            ServicesOfferedAffectedByIncidentSerializer)
from django.db.models import Q, F
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework import viewsets


class IncidentHistoryListViewSet(viewsets.ModelViewSet):
    model = IncidentHistory
    queryset = IncidentHistory.objects.all().order_by('start_date')
    serializer_class = IncidentHistoryListSerializer 


class IncidentHistoryViewSet(viewsets.ModelViewSet):
    model = IncidentHistory
    queryset = IncidentHistory.objects.all().order_by('start_date')
    serializer_class = IncidentHistorySerializer 


class ServicesOfferedAffectedByIncidentViewSet(viewsets.ModelViewSet):
    model = IncidentHistory
    queryset = IncidentHistory.objects.all()
    serializer_class = ServicesOfferedAffectedByIncidentSerializer 



