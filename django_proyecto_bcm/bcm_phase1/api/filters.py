from rest_framework import filters
from django.db.models import Q, F
# from django.utils.timezone import utc
# from datetime import datetime, timedelta

"""
    Filter example
"""
"""
class AlmacenFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        almacen = request.GET.get('almacen')
        if almacen:
            queryset = queryset.filter(almacenes__in=almacen)
        return queryset
"""
