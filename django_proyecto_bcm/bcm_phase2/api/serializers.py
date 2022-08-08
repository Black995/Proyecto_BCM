from bcm_phase2.models import ServiceOffered, ServiceUsed, Staff, InterestedParty,OrganizationActivity, SO_S
from configuration.models import ScaleView
from rest_framework import serializers
from django.db.models import F, Q
from bcm_phase1.api.serializers import RiskSerializer
from configuration.api.serializers import HeadquarterSerializer



class StaffListSerializer(serializers.ModelSerializer):
    area_name = serializers.CharField(read_only=True, source="area.name")
    position_name = serializers.CharField(read_only=True, source="position.name")
    headquarter_name = serializers.CharField(read_only=True, source="headquarter.name")

    class Meta:
        model = Staff
        fields = [
            'id',
            'staff_number',
            'names',
            'surnames',
            'earnings',
            'area',
            'area_name',
            'position',
            'position_name',
            'headquarter',
            'headquarter_name',
        ]


class StaffSerializer(serializers.ModelSerializer):
    area_name = serializers.CharField(read_only=True, source="area.name")
    position_name = serializers.CharField(read_only=True, source="position.name")
    headquarter_name = serializers.CharField(read_only=True, source="headquarter.name")
    user_email = serializers.CharField(read_only=True, source="user_staff.email")

    class Meta:
        model = Staff
        fields = [
            'id',
            'staff_number',
            'names',
            'surnames',
            'earnings',
            'area',
            'area_name',
            'position',
            'position_name',
            'headquarter',
            'headquarter_name',
            'user_staff',
            'user_email'
        ]


class ServiceOfferedListSerializer(serializers.ModelSerializer):
    type_name = serializers.SerializerMethodField(read_only=True)
    area_name = serializers.CharField(read_only=True)
    scale_max_value = serializers.CharField(read_only=True)

    class Meta:
        model = ServiceOffered
        fields = [
            'id',
            'name',
            'type',
            'type_name',
            'profit',
            'recovery_time',
            'recovery_point',
            'maximum_recovery_time',
            'criticality',
            'area',
            'area_name',
            'scale',
            'scale_max_value',
        ]

    def get_type_name(self, obj):
        return dict(ServiceOffered.TYPE).get(obj.type)
    
    def validate(self, attrs):
        # Se trae la escala de la vista para validar el mínimo RTO para la criticidad
        scale_view = ScaleView.objects.filter(name="Servicios de la Organización").first() if ScaleView.objects.filter(name="Servicios de la Organización") else None

        recovery_time = attrs.get('recovery_time')
        criticality = attrs.get('criticality')

        if(scale_view):
            if(criticality >= scale_view.minimum_scale_value and recovery_time >= scale_view.minimum_recovery_time):
                raise serializers.ValidationError( 
                    'La criticidad ingresada es superior al mínimo tolerable para el RTO ingresado')
            else:
                return super().validate(attrs)
        else:
            return super().validate(attrs)


class ServiceOfferedSerializer(serializers.ModelSerializer):
    type_name = serializers.SerializerMethodField(read_only=True)
    area_name = serializers.CharField(read_only=True, source="area.name")
    scale_name = serializers.CharField(read_only=True, source="scale.name")
    scale_min_value = serializers.CharField(
        read_only=True, source="scale.min_value")
    scale_max_value = serializers.CharField(
        read_only=True, source="scale.max_value")
    # El staffs funciona para llenar los elementos del many to many
    staffs = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True)
    # Serializer aninado
    _staffs = StaffSerializer(many=True, read_only=True)
    # El risks funciona para llenar los elementos del many to many
    risks = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True)
    # Serializer aninado
    _risks = RiskSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceOffered
        fields = [
            'id',
            'name',
            'type',
            'type_name',
            'profit',
            'recovery_time',
            'recovery_point',
            'maximum_recovery_time',
            'criticality',
            'area',
            'area_name',
            'scale',
            'scale_name',
            'scale_min_value',
            'scale_max_value',
            'staffs',
            '_staffs',
            'risks',
            '_risks'
        ]

    def get_type_name(self, obj):
        return dict(ServiceOffered.TYPE).get(obj.type)
    
    def validate(self, attrs):
        # Se trae la escala de la vista para validar el mínimo RTO para la criticidad
        scale_view = ScaleView.objects.filter(name="Servicios de la Organización").first() if ScaleView.objects.filter(name="Servicios de la Organización") else None

        recovery_time = attrs.get('recovery_time')
        criticality = attrs.get('criticality')

        if(scale_view):
            if(criticality >= scale_view.minimum_scale_value and recovery_time >= scale_view.minimum_recovery_time):
                raise serializers.ValidationError( 
                    'La criticidad ingresada es superior al mínimo tolerable para el RTO ingresado')
            else:
                return super().validate(attrs)
        else:
            return super().validate(attrs)


class ServiceUsedListSerializer(serializers.ModelSerializer):
    type_name = serializers.SerializerMethodField(read_only=True)
    scale_max_value = serializers.CharField(read_only=True)

    class Meta:
        model = ServiceUsed
        fields = [
            'id',
            'name',
            'type',
            'type_name',
            'spending',
            'criticality',
            'agreement_comment',
            'scale',
            'scale_max_value',
        ]

    def get_type_name(self, obj):
        return dict(ServiceUsed.TYPE).get(obj.type)


class ServiceUsedSerializer(serializers.ModelSerializer):
    type_name = serializers.SerializerMethodField(read_only=True)
    scale_name = serializers.CharField(read_only=True)
    scale_min_value = serializers.CharField(read_only=True)
    scale_max_value = serializers.CharField(read_only=True)
    # El service_offered funciona para llenar los elementos del many to many
    services_offered = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True)
    # Serializer aninado
    _services_offered = ServiceOfferedSerializer(many=True, read_only=True)
    # El risks funciona para llenar los elementos del many to many
    risks = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True)
    # Serializer aninado
    _risks = RiskSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceUsed
        fields = [
            'id',
            'name',
            'type',
            'type_name',
            'spending',
            'criticality',
            'agreement_comment',
            'scale',
            'scale_name',
            'scale_min_value',
            'scale_max_value',
            'services_offered',
            '_services_offered',
            'risks',
            '_risks'
        ]

    def get_type_name(self, obj):
        return dict(ServiceUsed.TYPE).get(obj.type)

class StaffListSerializer(serializers.ModelSerializer):
    area_name = serializers.CharField(read_only=True)
    position_name = serializers.CharField(read_only=True)

    class Meta:
        model = Staff
        fields = [
            'id',
            'staff_number',
            'names',
            'surnames',
            'earnings',
            'area',
            'area_name',
            'position',
            'position_name',
            'headquarter'
        ]


class StaffSerializer(serializers.ModelSerializer):
    area_name = serializers.CharField(read_only=True, source="area.name")
    position_name = serializers.CharField(read_only=True, source="position.name")
    headquarter_name = serializers.CharField(read_only=True, source="headquarter.name")
    user_email = serializers.CharField(read_only=True, source="user_staff.email")

    class Meta:
        model = Staff
        fields = [
            'id',
            'staff_number',
            'names',
            'surnames',
            'earnings',
            'area',
            'area_name',
            'position',
            'position_name',
            'headquarter',
            'headquarter_name',
            'user_email'
        ]

class OrganizationActivityListSerializer(serializers.ModelSerializer):
    scale_max_value = serializers.CharField(read_only=True)

    class Meta:
        model = OrganizationActivity
        fields =[
            'id',
            'name',
            'description',
            'cost',
            'recovery_time',
            'criticality',
            'scale',
            'scale_max_value'
        ]

class OrganizationActivitySerializer(serializers.ModelSerializer):
    scale_name = serializers.CharField(read_only=True)
    scale_min_value = serializers.CharField(read_only=True, source="scale.min_value")
    scale_max_value = serializers.CharField(read_only=True, source="scale.max_value")
    
    services_offered = serializers.ListField(
        child=serializers.IntegerField(),required=False,write_only=True)
    _services_offered = ServiceOfferedSerializer(many=True,read_only=True)

    risks = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True)
    _risks = RiskSerializer(many=True, read_only=True)
    
    headquarters = serializers.ListField(
        child=serializers.IntegerField(),required=False,write_only=True)
    _headquarters = HeadquarterSerializer(many=True,read_only=True)

    class Meta:
        model = OrganizationActivity
        fields = [
            'id',
            'name',
            'description',
            'cost',
            'recovery_time',
            'criticality',
            'services_offered',
            '_services_offered',
            'scale',
            'scale_name',
            'scale_min_value',
            'scale_max_value',
            'risks',
            '_risks',
            'headquarters',
            '_headquarters',
        ]


class InterestedPartyListSerializer(serializers.ModelSerializer):
    type_name = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = InterestedParty
        fields =[
            'id',
            'name',
            'type',
            'type_name',
            'description'
        ]

class interestedPartySerializer(serializers.ModelSerializer):
    type_name = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = InterestedParty
        fields = [
            'id',
            'name',
            'type',
            'type_name',
            'description',
        ] 


class SO_SSerializer(serializers.ModelSerializer):
    staff_number = serializers.CharField(read_only=True, source="staff.staff_number")
    staff_names = serializers.CharField(read_only=True, source="staff.names")
    staff_surnames = serializers.CharField(read_only=True, source="staff.surnames")
    staff_area_name = serializers.CharField(read_only=True, source="staff.area_name")
    staff_position_name = serializers.CharField(read_only=True, source="staff.position_name")
    staff_headquarter_name = serializers.CharField(read_only=True, source="staff.headquarter_name")

    class Meta:
        model = SO_S
        fields = [
            'id',
            'relevant',
            'service_offered',
            'staff',
            'staff_number',
            'staff_names',
            'staff_surnames',
            'staff_area_name',
            'staff_position_name',
            'staff_headquarter_name',
        ] 


    def create(self, instance, validated_data):
        simcard_nueva = validated_data.get('simcard', instance.simcard)
        numero_cuenta_nuevo = validated_data.get(
            "numero_cuenta", instance.numero_cuenta)

        if instance.simcard != simcard_nueva:
            Hist_Simcard.objects.create(tipo=3, simcard=simcard_nueva)


        instance.simcard = simcard_nueva
        instance.numero_cuenta = numero_cuenta_nuevo

        if instance.numero_cuenta:
            if instance.cliente:
                instance.cuenta, created = Cuenta.objects.get_or_create(
                    numero=instance.numero_cuenta)
            else:
                raise serializers.ValidationError(
                    {"numero_cuenta": "El Pos debe estar asignado a un cliente"})

        instance.save()

        return instance

