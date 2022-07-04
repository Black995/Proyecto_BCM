from django.urls import path

from .views import (InterestedPartyListViewSet, InterestedPartyViewSet, ServiceOfferedListViewSet, ServiceOfferedViewSet,
                    ServiceUsedListViewSet, ServiceUsedViewSet, StaffListViewSet,
                    StaffViewSet,OrganizationActivityListViewSet,OrganizationActivityViewSet)


urlpatterns = [
    path('services/offered/', ServiceOfferedListViewSet.as_view({
        'get': 'list',
        'post': 'create'}), name='service_offered_list'),
    path('service/offered/<int:pk>/', ServiceOfferedViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'}), name='service_offered_detail'),
    path('services/used/', ServiceUsedListViewSet.as_view({
        'get': 'list',
        'post': 'create'}), name='service_used_list'),
    path('service/used/<int:pk>/', ServiceUsedViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'}), name='service_used_detail'),
    path('staffs/', StaffListViewSet.as_view({
        'get': 'list',
        'post': 'create'}), name='staff_list'),
    path('staff/<int:pk>/', StaffViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'}), name='staff_detail'),
    path('organizationActivities/', OrganizationActivityListViewSet.as_view({
        'get':'list',
        'post':'create'}), name='activity_list'),
    path('organizationActivity/<int:pk>/', OrganizationActivityViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'}), name='activity_detail'),
    path('interestedParties/', InterestedPartyListViewSet.as_view({
        'get':'list',
        'post':'create'}), name='party_list'),
    path('interestedParty/<int:id>/', InterestedPartyViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'}), name='party_detail')
    
]
