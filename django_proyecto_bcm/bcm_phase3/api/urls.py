from django.urls import path
from .views import (IncidentHistoryListViewSet, IncidentHistoryViewSet, 
                    RisksAffectedByIncidentViewSet, ServicesOfferedAffectedByIncidentViewSet,
                    ServicesUsedAffectedByIncidentViewSet, OrganizationActivitiesAffectedByIncidentViewSet,
                    ContingencyPlanCreateViewSet, ContingencyPlanViewSet)

 

urlpatterns = [
    path('incident-histories/', IncidentHistoryListViewSet.as_view({
        'get': 'list',
        'post': 'create'}), name='incident_history_list'),
    path('incident-history/<int:pk>/', IncidentHistoryViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'}), name='incident_history_detail'),
    path('incident-history/risks/all/', RisksAffectedByIncidentViewSet.as_view({
        'get': 'list'}), name='incident_history_affected_risks_all'),
    path('incident-history/services-offered/all/', ServicesOfferedAffectedByIncidentViewSet.as_view({
        'get': 'list'}), name='incident_history_services_offered_all'),
    path('incident-history/services-used/all/', ServicesUsedAffectedByIncidentViewSet.as_view({
        'get': 'list'}), name='incident_history_services_used_all'),
    path('incident-history/organization-activities/all/', OrganizationActivitiesAffectedByIncidentViewSet.as_view({
        'get': 'list'}), name='incident_history_organization_activities_all'),
    path('incident-history/risks/<int:pk>/', RisksAffectedByIncidentViewSet.as_view({
        'get': 'retrieve'}), name='incident_history_affected_risks'),
    path('incident-history/services-offered/<int:pk>/', ServicesOfferedAffectedByIncidentViewSet.as_view({
        'get': 'retrieve'}), name='incident_history_services_offered'),
    path('incident-history/services-used/<int:pk>/', ServicesUsedAffectedByIncidentViewSet.as_view({
        'get': 'retrieve'}), name='incident_history_services_used'),
    path('incident-history/organization-activities/<int:pk>/', OrganizationActivitiesAffectedByIncidentViewSet.as_view({
        'get': 'retrieve'}), name='incident_history_organization_activities'),
    path('contingency-plan-create/', ContingencyPlanCreateViewSet.as_view({
        'put': 'update',
        'patch': 'partial_update'}), name='contingency_plan_create'),
    path('contingency-plan-detail/', ContingencyPlanViewSet.as_view({
        'get': 'list'}), name='contingency_plan_list'),
]
