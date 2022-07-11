from users.models import User
from bcm_phase2.models import Staff
from django.contrib.auth.models import Permission, Group
from rest_framework import serializers
from django.db.models import F, Q




class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = [
            'id',
            'name',
            'content_type_id',
            'codename',
        ]


class GroupListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Group
        fields = [
            'id',
            'name',
        ]

class GroupSerializer(serializers.ModelSerializer):
    # Serializer aninado
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = [
            'id',
            'name',
            'permissions',
        ]
        
        
class UserListSerializer(serializers.ModelSerializer):
    staff_number = serializers.CharField(read_only=True, source="staff.staff_number")
    names = serializers.CharField(read_only=True, source="staff.names")
    surnames = serializers.CharField(read_only=True, source="staff.surnames")

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
            'surnames'
        ]


class UserSerializer(serializers.ModelSerializer):
    staff_number = serializers.CharField(read_only=True, source="staff.staff_number")
    names = serializers.CharField(read_only=True, source="staff.names")
    surnames = serializers.CharField(read_only=True, source="staff.surnames")
    area_name = serializers.CharField(read_only=True, source="staff.area.name")
    position_name = serializers.CharField(read_only=True, source="staff.position.name")
    headquarter_name = serializers.CharField(read_only=True, source="staff.headquarter.name")
    # Serializer aninado
    permissions = PermissionSerializer(many=True, read_only=True)

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
            'area_name',
            'position_name',
            'headquarter_name',
            'permissions',
        ]


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

        