from users.models import User
from bcm_phase2.models import Staff
from django.contrib.auth.models import Permission, Group
from .serializers import (UserListSerializer, UserSerializer, StaffsWithoutUserSerializer, GroupListSerializer, 
                            GroupSerializer, PermissionSerializer, ChangePasswordSerializer, ProfileSerializer,
                            RecoverAccountSerializer, ResetPasswordSerializer)
from django.db.models import Q, F
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework.generics import (RetrieveAPIView)
from rest_framework import viewsets


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
    queryset = Permission.objects.annotate(model_name=F('content_type__model')).order_by('model_name', 'name')
    serializer_class = PermissionSerializer


class GroupListViewSet(viewsets.ModelViewSet):
    model = Group
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupListSerializer


class GroupViewSet(viewsets.ModelViewSet):
    model = Group
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return super().get_permissions()


class ProfileView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        self.kwargs['pk'] = request.user.id
        return super().retrieve(request, *args, **kwargs)


class ChangePasswordViewSet(viewsets.ModelViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return super().get_permissions()


class RecoverAccountViewSet(viewsets.ModelViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = RecoverAccountSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return super().get_permissions()


class ResetPasswordViewSet(viewsets.ModelViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = ResetPasswordSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return super().get_permissions()
