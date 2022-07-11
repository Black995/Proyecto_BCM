from users.models import User
from bcm_phase2.models import Staff
from django.contrib.auth.models import Permission, Group
from .serializers import UserListSerializer, UserSerializer, StaffsWithoutUserSerializer, GroupListSerializer, GroupSerializer, PermissionSerializer
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from django.db.models import Q, F


class UserListViewSet(viewsets.ModelViewSet):
    model = User
    queryset = User.objects.all().order_by('email')
    serializer_class = UserListSerializer 

    
class UserViewSet(viewsets.ModelViewSet):
    model = User
    queryset = User.objects.all().order_by('email')
    serializer_class = UserSerializer 


class StaffsWithoutUserViewSet(viewsets.ModelViewSet):
    model = Staff
    queryset = Staff.objects.filter(user_staff__isnull=True).order_by('names')
    serializer_class = StaffsWithoutUserSerializer 


class PermissionViewSet(viewsets.ModelViewSet):
    model = Permission
    queryset = Permission.objects.all().order_by('name')
    serializer_class = PermissionSerializer


class GroupListViewSet(viewsets.ModelViewSet):
    model = Group
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupListSerializer


class GroupViewSet(viewsets.ModelViewSet):
    model = Group
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer

