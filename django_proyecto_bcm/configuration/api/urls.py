from django.urls import path

from .views import (AreaViewSet, ScaleViewSet, ScaleviewViewSet)


urlpatterns = [
    path('areas/', AreaViewSet.as_view({
        'get': 'list',
        'post': 'create'}), name='area_list'),
    path('area/<int:pk>/', AreaViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'}), name='area_detail'),
    path('scales/', ScaleViewSet.as_view({
        'get': 'list',
        'post': 'create'}), name='scale_list'),
    path('scale/<int:pk>/', ScaleViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'}), name='scale_detail'),
    path('scales/view/', ScaleviewViewSet.as_view({
        'get': 'list',
        'post': 'create'}), name='scale_view_list'),
    path('scale/view/<int:pk>/', ScaleviewViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'}), name='scale_view_detail'),
]
