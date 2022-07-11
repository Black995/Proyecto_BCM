from django.urls import path
from .views import (UserListViewSet, UserViewSet, StaffsWithoutUserViewSet,
                    PermissionViewSet, GroupListViewSet, GroupViewSet)


 

urlpatterns = [
    path('users/', UserListViewSet.as_view({
        'get': 'list',
        'post': 'create'}), name='user_list'),
    path('user/<int:pk>/', UserViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'}), name='user_detail'),
    path('staffs-without-user/', StaffsWithoutUserViewSet.as_view({
        'get': 'list'}), name='staffs_without_user_list'),
    path('groups/', GroupListViewSet.as_view({
        'get': 'list',
        'post': 'create'}), name='group_list'),
    path('group/<int:pk>/', GroupViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'}), name='group_detail'),
    path('permissions/', PermissionViewSet.as_view({
        'get': 'list',
        'post': 'create'}), name='permission_list'),
]
