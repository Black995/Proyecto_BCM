from django.urls import path

from .views import (ServiceOfferedListViewSet, ServiceOfferedViewSet)


urlpatterns = [
    path('services/offered/', ServiceOfferedListViewSet.as_view({
        'get': 'list',
        'post': 'create'}), name='service_offered_list'),
    path('service/offered/<int:pk>/', ServiceOfferedViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'}), name='service_offered_detail'),
]
