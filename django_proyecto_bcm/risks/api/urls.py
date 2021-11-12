from django.urls import path

from .views import (RiskViewSet)


urlpatterns = [

    path('risks/', RiskViewSet.as_view({
        'get': 'list',
        'post': 'create'}), name='risk_list'),
    path('risk/<int:pk>/', RiskViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'}), name='risk_detail'),

]
