from rest_framework import filters
from django.db.models import Q, F
from configuration.models import ScaleView, Scale
from django.utils.timezone import utc
from datetime import datetime, timedelta


class ScaleViewFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        name = request.GET.get('name')
        if name:
            print('nombre de la escala: ', name)
            # Verificamos que exista el nombre. Si no existe, entonces filtramos por defecto con
            # la escala con nombre "default"
            try:
                scale_view = ScaleView.objects.filter(name=name)
            except ScaleView.DoesNotExist:
                scale_view = None
            print('escala')
            if(scale_view):
                print(name)
                queryset = queryset.filter(name=name)
            else:
                print('default')
                queryset = queryset.filter(name='default')
        return queryset
