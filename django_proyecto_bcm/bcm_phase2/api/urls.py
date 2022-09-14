from django.urls import path

from .views import (InterestedPartyListViewSet, InterestedPartyViewSet, ServiceOfferedListViewSet, ServiceOfferedViewSet,
                    ServiceUsedListViewSet, ServiceUsedViewSet, StaffListViewSet,
                    StaffViewSet,OrganizationActivityListViewSet,OrganizationActivityViewSet, 
                    SO_SViewSet, ServiceOfferedWithStaffsViewSet, download_excel_massive_load_staff)


urlpatterns = [
    path('services/offered/', ServiceOfferedListViewSet.as_view({
        'get': 'list',
        'post': 'create'}), name='service_offered_list'),
    path('service/offered/<int:pk>/', ServiceOfferedViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'}), name='service_offered_detail'),
    path('service-offered/staffs/<int:pk>/', ServiceOfferedWithStaffsViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update'}), name='service_offered_with_staffs'),
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
    path('staffs/download_excel_massive_load_staff/', download_excel_massive_load_staff.as_view(),
         name='download_excel_massive_load_staff'),
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
    path('interestedParty/<int:pk>/', InterestedPartyViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'}), name='party_detail'),
    path('service_offered_staffs/', SO_SViewSet.as_view({
        'get':'list',
        'post':'create'}), name='so_s_list'),
    path('service_offered_staff/<int:id>/', SO_SViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'}), name='so_s_detail')
    
]
