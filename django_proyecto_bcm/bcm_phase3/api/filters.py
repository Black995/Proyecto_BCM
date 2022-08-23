from rest_framework import filters
from django.db.models import Q, F
from bcm_phase3.models import IncidentHistory
from django.utils.timezone import utc
from datetime import datetime, timedelta


class IncidentDatesFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if not start_date or not end_date:
            return queryset
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1, seconds=-1)
        return queryset.filter(start_date__gte=start_date, start_date__lte=end_date)

        
class ContingencyPlanByCrisisScenarioFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        crisis_scenario = request.GET.get('crisis_scenario')
        if not crisis_scenario:
            return queryset
        return queryset.filter(crisis_scenario=crisis_scenario)