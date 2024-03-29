from django.urls import path

from .views import (RiskViewSet, CrisisScenarioViewSet, CrisisScenarioListViewSet, 
                    CrisisScenarioListRisksViewSet, ServicesOfferedRiskListViewSet,
                    DownloadCrisisScenarioDocument)


urlpatterns = [
    path('risks/', RiskViewSet.as_view({
        'get': 'list',
        'post': 'create'}), name='risk_list'),
    path('risk/<int:pk>/', RiskViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'}), name='risk_detail'),
    path('crisis_scenarios_list/', CrisisScenarioListViewSet.as_view({
        'get': 'list'}), name='crisis_scenarios_list'),
    path('crisis_scenarios/', CrisisScenarioViewSet.as_view({
        'post': 'create'}), name='crisis_scenarios_create'),
    path('crisis_scenario/<int:pk>/', CrisisScenarioViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'}), name='crisis_scenario_detail'),
    path('download_crisis_scenario_document/<int:id>/',
         DownloadCrisisScenarioDocument.as_view(), name='download_crisis_scenario_document'),
    path('crisis_scenarios_list_risks/', CrisisScenarioListRisksViewSet.as_view({
        'get': 'list'}), name='crisis_scenarios_list_risks'),
    path('service_offered_risks_list/', ServicesOfferedRiskListViewSet.as_view({
        'get': 'list'}), name='service_offered_risks_list'),
]
