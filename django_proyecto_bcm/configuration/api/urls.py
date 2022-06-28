from django.urls import path

from .views import (AreaViewSet, ScaleViewSet, ScaleviewViewSet, PositionViewSet, 
    HeadquarterViewSet, StateViewSet, CityViewSet, TownshipViewSet, ParishViewSet)


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
    path('positions/', PositionViewSet.as_view({
        'get': 'list',
        'post': 'create'}), name='position_list'),
    path('position/<int:pk>/', PositionViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'}), name='position_detail'),
    path('headquarters/', HeadquarterViewSet.as_view({
        'get': 'list',
        'post': 'create'}), name='headquarter_list'),
    path('headquarter/<int:pk>/', HeadquarterViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'}), name='headquarter_detail'),

    # Requests de estados, ciudades, municipios y parroquias
    path('states/', StateViewSet.as_view({
        'get': 'list'}), name='state_list'),
    path('cities/', CityViewSet.as_view({
        'get': 'list'}), name='city_list'),
    path('townships/', TownshipViewSet.as_view({
        'get': 'list'}), name='township_list'),
    path('parishes/', ParishViewSet.as_view({
        'get': 'list'}), name='parish_list'),
]
