from rest_framework import filters
from django.db.models import Q, F
from configuration.models import ScaleView, State, City, Township, Parish
from django.utils.timezone import utc
from datetime import datetime, timedelta


class ScaleViewFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        name = request.GET.get('name')
        if name:
            # Verificamos que exista el nombre. Si no existe, entonces filtramos por defecto con
            # la escala con nombre "default"
            try:
                scale_view = ScaleView.objects.filter(name=name)
            except ScaleView.DoesNotExist:
                scale_view = None
            if(scale_view):
                queryset = queryset.filter(name=name)
            else:
                queryset = queryset.filter(name='default')
        return queryset


class CityTownshipFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        state_id = request.GET.get('state_id')
        if state_id:
            queryset = queryset.filter(state=state_id)
        return queryset


class ParishFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        township_id = request.GET.get('township_id')
        if township_id:
            queryset = queryset.filter(township=township_id)
        return queryset

