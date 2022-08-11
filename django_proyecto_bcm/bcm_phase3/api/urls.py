from django.urls import path
from .views import (IncidentHistoryListViewSet, IncidentHistoryViewSet, ServicesOfferedAffectedByIncidentViewSet)

 

urlpatterns = [
    path('incident-histories/', IncidentHistoryListViewSet.as_view({
        'get': 'list',
        'post': 'create'}), name='user_list'),
    path('incident-history/<int:pk>/', IncidentHistoryViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'}), name='user_detail'),
    path('incident-history/services-offered/<int:pk>/', ServicesOfferedAffectedByIncidentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'}), name='user_detail'),
]
