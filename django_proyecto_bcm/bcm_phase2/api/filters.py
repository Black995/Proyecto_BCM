from rest_framework import filters
from django.db.models import Q, F
from bcm_phase2.models import SO_S


class SO_SFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        service_id = request.GET.get('service_id')
        if service_id:
            queryset = queryset.filter(service_offered=service_id)
        return queryset

class R_SOFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self,request,queryset,view):
        ressource_id = request.GET.get('ressource_id')
        if ressource_id:
            queryset = queryset.filter(ressource=ressource_id)
        return queryset
