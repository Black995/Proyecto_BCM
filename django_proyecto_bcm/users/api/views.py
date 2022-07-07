from users.models import User
from bcm_phase2.models import Staff
from .serializers import UserListSerializer, UserSerializer, StaffsWithoutUserSerializer
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

