from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.password_validation import \
    validate_password as django_validate_password
from django.core.exceptions import ValidationError
from erm_api.serializers import ENTITY_FIELDS, EntitySerializer
from rest_framework import serializers

User = get_user_model()


class UserSerializer(EntitySerializer):

    class Meta:
        model = User
        fields = ENTITY_FIELDS + [
            'email',
            'password',
            'first_name',
            'second_name',
            'last_name',
            'second_last_name',
            'role',
            'role_name',
            'is_substitute',
            'last_login',
            'areas',
        ]
        read_only_fields = (
            'role_name',
            'last_login',
            'areas',
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }


class GroupSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _permissions = serializers.ListField(
        required=False, child=serializers.CharField())

    class Meta:
        model = Group
        fields = [
            'id',
            'name',
            '_permissions',
        ]
        read_only_fields = [
            'id'
            'name',
        ]

    def get_name(self, obj):
        return dict(User.ROLES).get(obj.id)

    def to_representation(self, instance):
        instance._permissions = instance.permissions.values_list(
            'codename', flat=True)
        return super().to_representation(instance)

    def update(self, instance, validated_data):
        if '_permissions' in validated_data:
            permissions = validated_data.pop('_permissions')
            permissions = Permission.objects.filter(
                codename__in=permissions).values_list('pk', flat=True)
            instance.permissions.clear()
            instance.permissions.add(*permissions)
        return super().update(instance, validated_data)


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = [
            'id',
            'name',
            'codename',
        ]
        read_only_fields = [
            'id',
            'name',
            'codename',
        ]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        user = self.context['request'].user
        django_validate_password(value, user)
        return value

    def save(self, **kwargs):
        try:
            user = self.context['request'].user
            old_password = self.validated_data['old_password']
            new_password = self.validated_data['new_password']
            user.change_password(old_password, new_password)
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)


class RecoverAccountSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def save(self, **kwargs):
        email = self.validated_data['email']
        user = User.objects.filter(email=email).first()
        if user is not None:
            user.send_password_reset_email()


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def save(self, **kwargs):
        try:
            User.reset_password(
                self.validated_data['token'],
                self.validated_data['password']
            )
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
