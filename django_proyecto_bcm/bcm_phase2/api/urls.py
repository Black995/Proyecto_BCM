from django.urls import path

from bcm_phase2.api.filters import R_SOFilterBackend

from .views import (InterestedPartyListViewSet, InterestedPartyViewSet, R_SOViewSet, ServiceOfferedListViewSet, ServiceOfferedViewSet,
                    ServiceUsedListViewSet, ServiceUsedViewSet, StaffListViewSet,
                    StaffViewSet,OrganizationActivityListViewSet,OrganizationActivityViewSet, 
                    SO_SViewSet, ServiceOfferedWithStaffsViewSet, download_bulk_upload_template, BulkUploadStaffViewSet,
                    RessourceWithServiceOfferedViewSet, RessourceViewSet, RessourceListViewSet,GenerateServiceOffered)

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'staff_bulk_upload', BulkUploadStaffViewSet)


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
    path('staff/bulk_upload_template/', download_bulk_upload_template.as_view(),
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
        'delete': 'destroy'}), name='so_s_detail'),
    path('ressources/', RessourceListViewSet.as_view({
        'get':'list',
        'post':'create'}), name='resource_list'),
    path('ressources/<int:pk>/', RessourceViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'}), name='ressource_detail'),
    path('ressources_service_offered1/<int:pk>/', RessourceWithServiceOfferedViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',}), name='ressource_with_service_offered'),
    path('ressources_service_offered/', R_SOViewSet.as_view({
        'get':'list',
        'post':'create'}), name='r_so_list'),
    path('ressource_service_offered/<int:id>/', R_SOViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'}), name='r_so_detail'),
    path('service_offered_report/', GenerateServiceOffered.as_view(), 
            name='service_offered_report')
]

urlpatterns += router.urls
