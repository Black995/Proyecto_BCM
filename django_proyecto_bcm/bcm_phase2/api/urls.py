from django.urls import path

from .views import (ServiceOfferedListViewSet, ServiceOfferedViewSet,
                    ServiceUsedListViewSet, ServiceUsedViewSet)


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
]
