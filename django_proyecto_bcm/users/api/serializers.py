from users.models import User
from bcm_phase2.models import Staff
from django.contrib.auth.models import Permission, Group
from rest_framework import serializers
from django.db.models import F, Q
from django.contrib.auth.password_validation import \
    validate_password as django_validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _




class PermissionSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    model_name = serializers.CharField(read_only=True, source="content_type.model")
    model_name_es = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Permission
        fields = [
            'id',
            'name',
            'codename',
            'model_name',
            'model_name_es',
        ]

    def get_name(self, obj):
        return _(obj.name)
        
    def get_model_name_es(self, obj):
        return _(obj.content_type.model)


class GroupListSerializer(serializers.ModelSerializer):
    _permissions = serializers.ListField(
        required=False, child=serializers.CharField(), write_only=True)
    
    class Meta:
        model = Group
        fields = [
            'id',
            'name',
            '_permissions',
        ]
        
    def to_representation(self, instance):
        instance._permissions = instance.permissions.values_list(
            'codename', flat=True)
        return super().to_representation(instance)
        
    def create(self, validated_data):
        permissions = validated_data.pop('_permissions')
        group = Group.objects.create(**validated_data)
        if permissions:
            permissions = Permission.objects.filter(
                codename__in=permissions).values_list('pk', flat=True)
            group.permissions.add(*permissions)
        return group


class GroupSerializer(serializers.ModelSerializer):
    # Serializer aninado
    permissions = PermissionSerializer(many=True, read_only=True)
    _permissions = serializers.ListField(
        required=False, child=serializers.CharField(), write_only=True)

    class Meta:
        model = Group
        fields = [
            'id',
            'name',
            'permissions',
            '_permissions',
        ]
    
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

            # Una vez actualizados los permisos de los grupos, actualizamos 
            # los permisos de los usuarios
            users = User.objects.all()

            for user in users:
                groups = user.groups.all()
                user.user_permissions.clear()

                for group in groups:
                    for perm in group.permissions.all():
                        user.user_permissions.add(perm)

        return super().update(instance, validated_data)


                
class UserListSerializer(serializers.ModelSerializer):
    staff_number = serializers.CharField(read_only=True, source="staff.staff_number")
    names = serializers.CharField(read_only=True, source="staff.names")
    surnames = serializers.CharField(read_only=True, source="staff.surnames")
    _groups = serializers.ListField(
        required=False, child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'password',
            'is_active',
            'is_admin',
            'is_superuser',
            'staff',
            'staff_number',
            'names',
            'surnames',
            '_groups',
        ]

    def save(self, **kwargs):
        self.Meta.model.cleaned_data = self.validated_data
        try:
            return super().save(**kwargs)
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

    def to_representation(self, instance):
        instance._groups = instance.groups.values_list(
            'id', flat=True)
        instance._permissions = instance.groups.values_list(
            'id', flat=True)
        return super().to_representation(instance)
        
    def create(self, validated_data):
        groups = validated_data.pop('_groups')
        user = User.objects.create(**validated_data)
        # Asociar grupos al usuario
        if groups:
            groups = Group.objects.filter(
                id__in=groups).values_list('pk', flat=True)
            user.groups.add(*groups)
            
            # Asociar permisos de los grupos al usuario
            user.user_permissions.clear()
            permission_list = Group.objects.filter(
                id__in=groups).values_list('permissions', flat=True)
            permission_ids = []
            for perm in permission_list:
                if(not (perm in permission_ids)):
                    permission_ids.append(perm)
            user.user_permissions.add(*permission_list)
        return user


class UserSerializer(serializers.ModelSerializer):
    staff_number = serializers.CharField(read_only=True, source="staff.staff_number")
    names = serializers.CharField(read_only=True, source="staff.names")
    surnames = serializers.CharField(read_only=True, source="staff.surnames")
    area_name = serializers.CharField(read_only=True, source="staff.area.name")
    position_name = serializers.CharField(read_only=True, source="staff.position.name")
    headquarter_name = serializers.CharField(read_only=True, source="staff.headquarter.name")
    # Serializer aninado
    groups = GroupListSerializer(many=True, read_only=True)
    _groups = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'is_active',
            'is_admin',
            'is_superuser',
            'staff',
            'staff_number',
            'names',
            'surnames',
            'area_name',
            'position_name',
            'headquarter_name',
            'groups',
            '_groups',
        ]
            
    def save(self, **kwargs):
        self.Meta.model.cleaned_data = self.validated_data
        try:
            return super().save(update_fields=self.validated_data, **kwargs)
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

    def to_representation(self, instance):
        instance._groups = instance.groups.values_list(
            'id', flat=True)
        return super().to_representation(instance)

    def update(self, instance, validated_data):
        # Asociar grupos al usuario
        if '_groups' in validated_data:
            groups = validated_data.pop('_groups')
            groups = Group.objects.filter(
                id__in=groups).values_list('pk', flat=True)
            instance.groups.clear()
            instance.groups.add(*groups)

            # Asociar permisos de los grupos al usuario
            instance.user_permissions.clear()
            permission_list = Group.objects.filter(
                id__in=groups).values_list('permissions', flat=True)
            permission_ids = []
            for perm in permission_list:
                if(not (perm in permission_ids)):
                    permission_ids.append(perm)
            instance.user_permissions.add(*permission_list)
        return super().update(instance, validated_data)



class StaffsWithoutUserSerializer(serializers.ModelSerializer):
    area_name = serializers.CharField(read_only=True, source="area.name")
    position_name = serializers.CharField(read_only=True, source="position.name")

    class Meta:
        model = Staff
        fields = [
            'id',
            'names',
            'surnames',
            'area_name',
            'position_name',
        ]
        

class ProfileSerializer(serializers.ModelSerializer):
    staff_number = serializers.CharField(read_only=True, source="staff.staff_number")
    names = serializers.CharField(read_only=True, source="staff.names")
    surnames = serializers.CharField(read_only=True, source="staff.surnames")
    area = serializers.CharField(read_only=True, source="staff.area.id")
    area_name = serializers.CharField(read_only=True, source="staff.area.name")
    position = serializers.CharField(read_only=True, source="staff.position.id")
    position_name = serializers.CharField(read_only=True, source="staff.position.name")
    headquarter = serializers.CharField(read_only=True, source="staff.headquarter.id")
    headquarter_name = serializers.CharField(read_only=True, source="staff.headquarter.name")
    # Serializer aninado
    groups = GroupListSerializer(many=True, read_only=True)
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'password',
            'is_active',
            'is_admin',
            'is_superuser',
            'staff',
            'staff_number',
            'names',
            'surnames',
            'area',
            'area_name',
            'position',
            'position_name',
            'headquarter',
            'headquarter_name',
            'groups',
            'permissions'
        ]
            
    def get_permissions(self, obj):
        user = User.objects.get(id=obj.id)
        permissions = user.get_all_permissions()
        return permissions


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        user = self.context['request'].user
        django_validate_password(value, user)
        return value

    def save(self, **kwargs):
        try:
            print('changing password')
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