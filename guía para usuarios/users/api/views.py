from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.utils.translation import ugettext_lazy as _
from erm_api.views import BulkUploadViewSet, EntityViewSet
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from users.api.filters import UserFilter
from users.api.serializers import (ChangePasswordSerializer, GroupSerializer,
                                   PermissionSerializer,
                                   RecoverAccountSerializer,
                                   ResetPasswordSerializer, UserSerializer)

User = get_user_model()


class UserViewSet(EntityViewSet, BulkUploadViewSet):
    queryset = User.objects.all_with_deleted()
    serializer_class = UserSerializer
    filter_class = UserFilter

    bulk_upload_template_name = 'users.xlsm'

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated])
    def roles(self, request):
        return Response(dict(User.ROLES))

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated])
    def profile(self, request):
        user_data = UserSerializer(instance=request.user).data
        return Response(user_data)

    @action(methods=['POST'], detail=False, serializer_class=ChangePasswordSerializer, permission_classes=[IsAuthenticated])
    def change_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': _('Password changed successfully')})

    @action(methods=['POST'], detail=False, serializer_class=RecoverAccountSerializer, permission_classes=[AllowAny])
    def recover_account(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': _('Password recovery email sent')})

    @action(methods=['POST'], detail=False, serializer_class=ResetPasswordSerializer, permission_classes=[AllowAny])
    def reset_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': _('Password reset successfully')})


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    ordering_fields = ['pk']
    ordering = ['pk']

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return super().get_permissions()


class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    ordering_fields = ['pk']
    ordering = ['pk']

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return super().get_permissions()
