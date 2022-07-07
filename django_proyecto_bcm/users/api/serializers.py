from users.models import User
from bcm_phase2.models import Staff
from rest_framework import serializers
from django.db.models import F, Q


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

        