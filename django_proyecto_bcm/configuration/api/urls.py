from django.urls import path
from .views import (AreaViewSet, ProductActivatationListViewSet, ScaleViewSet, ScaleviewViewSet, PositionViewSet, 
    HeadquarterViewSet, StateViewSet, CityViewSet, TownshipViewSet, ParishViewSet,
    OrganizationViewSet,UsedKeysViewSet)


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

    # Request para crear a la primera empresa y traerla
    path('organizations/', OrganizationViewSet.as_view({
        'get': 'list',
        'post': 'create'}), name='organization_list'),
    # Request para detallar la empresa y actualizarla
    path('organization/<int:pk>/', OrganizationViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',}), name='organization_detail'),
    #Request para activacion del producto
    path('activate/',UsedKeysViewSet.as_view({
        'get':'list',
        'post': 'create'}),name='activate_product'),
    path('get_activation_state/',ProductActivatationListViewSet.as_view({
        'get':'list'}),name='get_product_activation')

    
]
