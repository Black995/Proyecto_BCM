from rest_framework import filters
from django.db.models import Q, F
from configuration.models import ScaleView, Scale
from django.utils.timezone import utc
from datetime import datetime, timedelta


class ScaleViewFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        name = request.GET.get('name')
        if name:
            queryset = queryset.filter(name=name)
        return queryset
