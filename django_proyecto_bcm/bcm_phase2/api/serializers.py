from curses.ascii import SO
from wsgiref.simple_server import server_version
from numpy import delete
from bcm_phase2.models import ServiceOffered, ServiceUsed, Staff, InterestedParty,OrganizationActivity, SO_S, Ressource, R_SO
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
            'phone_number_1',
            'phone_number_code_1',
            'phone_number_1_format_international',
            'phone_number_2',
            'phone_number_code_2',
            'phone_number_2_format_international',
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
    headquarter_city = serializers.CharField(read_only=True, source="headquarter.city.name")
    headquarter_parish = serializers.CharField(read_only=True, source="headquarter.parish.name")
    headquarter_township = serializers.CharField(read_only=True, source="headquarter.parish.township.name")
    headquarter_state = serializers.CharField(read_only=True, source="headquarter.city.state.name")
    user_email = serializers.CharField(read_only=True, source="user_staff.email")

    class Meta:
        model = Staff
        fields = [
            'id',
            'staff_number',
            'names',
            'surnames',
            'phone_number_1',
            'phone_number_code_1',
            'phone_number_1_format_international',
            'phone_number_2',
            'phone_number_code_2',
            'phone_number_2_format_international',
            'earnings',
            'area',
            'area_name',
            'position',
            'position_name',
            'headquarter',
            'headquarter_name',
            'headquarter_city',
            'headquarter_parish',
            'headquarter_township',
            'headquarter_state',
            #'user_staff',
            'user_email'
        ]


class SO_SSerializer(serializers.ModelSerializer):
    staff_number = serializers.CharField(read_only=True, source="staff.staff_number")
    staff_names = serializers.CharField(read_only=True, source="staff.names")
    staff_surnames = serializers.CharField(read_only=True, source="staff.surnames")
    staff_area_name = serializers.CharField(read_only=True, source="staff.area.name")
    staff_position_name = serializers.CharField(read_only=True, source="staff.position.name")
    staff_headquarter_name = serializers.CharField(read_only=True, source="staff.headquarter.name")
    staff_phone_number_code_1 = serializers.CharField(read_only=True, source="staff.phone_number_code_1")
    staff_phone_number_1_format_international = serializers.CharField(read_only=True, source="staff.phone_number_1_format_international")
    staff_phone_number_code_2 = serializers.CharField(read_only=True, source="staff.phone_number_code_2")
    staff_phone_number_2_format_international = serializers.CharField(read_only=True, source="staff.phone_number_2_format_international")

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
            'staff_phone_number_code_1',
            'staff_phone_number_1_format_international',
            'staff_phone_number_code_2',
            'staff_phone_number_2_format_international',
        ] 


class ServiceOfferedListSerializer(serializers.ModelSerializer):
    type_name = serializers.SerializerMethodField(read_only=True)
    area_name = serializers.CharField(read_only=True, source="area.name")
    scale_max_value = serializers.CharField(read_only=True, source="scale.max_value")

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


class ServiceOfferedWithStaffsSerializer(serializers.ModelSerializer):
    
    staffs_json = serializers.ListField(
        child=serializers.JSONField(), required=False)

    class Meta:
        model = ServiceOffered
        fields = [
            'id',
            'staffs_json'
        ]

    
    def update(self, instance, validated_data):
        id_service = validated_data.get('id', instance.id)
        staffs_json = validated_data.get('staffs_json')
        service = ServiceOffered.objects.get(id=id_service)

        """
            Si se envía el campo staff_json entonces se procede a crear los registros en 
            el modelo SO_S
        """
        if staffs_json is not None:
            SO_S.objects.filter(service_offered=service).delete()

            for s in staffs_json:
                staff = Staff.objects.get(id=s['staff'])

                SO_S.objects.create(
                    relevant=s['relevant'],
                    service_offered=service,
                    staff=staff
                )
                
        instance.save()
        return instance


class ServiceUsedListSerializer(serializers.ModelSerializer):
    type_name = serializers.SerializerMethodField(read_only=True)
    scale_max_value = serializers.CharField(read_only=True, source="scale.max_value")

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


class ServiceOfferedSerializer(serializers.ModelSerializer):
    type_name = serializers.SerializerMethodField(read_only=True)
    area_name = serializers.CharField(read_only=True, source="area.name")
    scale_name = serializers.CharField(read_only=True, source="scale.name")
    scale_min_value = serializers.CharField(
        read_only=True, source="scale.min_value")
    scale_max_value = serializers.CharField(
        read_only=True, source="scale.max_value")
    # El risks funciona para llenar los elementos del many to many
    risks = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True)
    # Serializer aninado
    _risks = RiskSerializer(many=True, read_only=True)
    staffs_json = serializers.ListField(
        child=serializers.JSONField(), required=False)
    # Serializer aninado
    service_offered_service_used = ServiceUsedListSerializer(many=True, read_only=True)

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
            'risks',
            '_risks',
            'staffs_json',
            'service_offered_service_used'
        ]

    def get_type_name(self, obj):
        return dict(ServiceOffered.TYPE).get(obj.type)
    
    def validate(self, attrs):
        # Se trae la escala de la vista para validar el mínimo RTO para la criticidad
        scale_view = ScaleView.objects.filter(name="Servicios de la Organización").first() if ScaleView.objects.filter(name="Servicios de la Organización") else None

        recovery_time = attrs.get('recovery_time')
        criticality = attrs.get('criticality')

        if(scale_view and recovery_time and criticality):
            if(criticality >= scale_view.minimum_scale_value and recovery_time >= scale_view.minimum_recovery_time):
                raise serializers.ValidationError( 
                    'El RTO ingresado supera el máximo tolerable para la criticidad ingresada')
            else:
                return super().validate(attrs)
        else:
            return super().validate(attrs)


class ServiceUsedSerializer(serializers.ModelSerializer):
    type_name = serializers.SerializerMethodField(read_only=True)
    scale_name = serializers.CharField(read_only=True, source="scale.name")
    scale_min_value = serializers.CharField(read_only=True, source="scale.min_value")
    scale_max_value = serializers.CharField(read_only=True, source="scale.max_value")
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

class OrganizationActivityListSerializer(serializers.ModelSerializer):
    scale_max_value = serializers.CharField(read_only=True, source="scale.max_value")

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
            
    def validate(self, attrs):
        # Se trae la escala de la vista para validar el mínimo RTO para la criticidad
        scale_view = ScaleView.objects.filter(name="Servicios de Soporte").first() if ScaleView.objects.filter(name="Servicios de Soporte") else None

        recovery_time = attrs.get('recovery_time')
        criticality = attrs.get('criticality')

        if(scale_view and recovery_time and criticality):
            if(criticality >= scale_view.minimum_scale_value and recovery_time >= scale_view.minimum_recovery_time):
                raise serializers.ValidationError( 
                    'La criticidad ingresada es superior al mínimo tolerable para el RTO ingresado')
            else:
                return super().validate(attrs)
        else:
            return super().validate(attrs)


class OrganizationActivitySerializer(serializers.ModelSerializer):
    scale_name = serializers.CharField(read_only=True, source="scale.name")
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

    def validate(self, attrs):
        # Se trae la escala de la vista para validar el mínimo RTO para la criticidad
        scale_view = ScaleView.objects.filter(name="Actividades de la Organización").first() if ScaleView.objects.filter(name="Actividades de la Organización") else None

        recovery_time = attrs.get('recovery_time')
        criticality = attrs.get('criticality')

        if(scale_view and recovery_time and criticality):
            if(criticality >= scale_view.minimum_scale_value and recovery_time >= scale_view.minimum_recovery_time):
                raise serializers.ValidationError( 
                    'La criticidad ingresada es superior al mínimo tolerable para el RTO ingresado')
            else:
                return super().validate(attrs)
        else:
            return super().validate(attrs)


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
    def get_type_name(self, obj):
        return dict(InterestedParty.TYPE).get(obj.type)

class interestedPartySerializer(serializers.ModelSerializer):
    type_name = serializers.SerializerMethodField(read_only = True)

    services_offered = serializers.ListField(
        child=serializers.IntegerField(),required=False,write_only=True)
    _services_offered = ServiceOfferedSerializer(many=True,read_only=True)

    services_used = serializers.ListField(
        child=serializers.IntegerField(),required=False,write_only=True)
    _services_used = ServiceUsedSerializer(many=True,read_only=True)

    class Meta:
        model = InterestedParty
        fields = [
            'id',
            'name',
            'type',
            'type_name',
            'description',
            "services_offered",
            "_services_offered",
            "services_used",
            "_services_used",
        ] 

    def get_type_name(self, obj):
        return dict(ServiceUsed.TYPE).get(obj.type)

class ServiceOfferedStaffSerializer(serializers.ModelSerializer):
    type_name = serializers.SerializerMethodField(read_only=True)
    area_name = serializers.CharField(read_only=True, source="area.name")
    # Serializer aninado
    staffs_service = SO_SSerializer(many=True, read_only=True, source="service_offered_so_s")
    # Serializer aninado
    service_offered_service_used = ServiceUsedListSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceOffered
        fields = [
            'id',
            'name',
            'type_name',
            'profit',
            'recovery_time',
            'recovery_point',
            'maximum_recovery_time',
            'criticality',
            'area_name',
            'staffs_service',
            'service_offered_service_used'
        ]

    def get_type_name(self, obj):
        return dict(ServiceOffered.TYPE).get(obj.type)

class RessourceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ressource
        fields = [
            'id',
            'name',
            'amount',
            'description'
        ]

class RessourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ressource
        fields =[
            'id',
            'name',
            'amount',
            'description'
        ]
class RessourceWithServiceOfferedSerializer(serializers.ModelSerializer):

    services_json = serializers.ListField(
        child = serializers.JSONField(), required=False)

    class Meta:
        model = Ressource
        fields = [
            'id',
            'services_json'
        ]
    
    def update(self, instance, validated_data):
        id_ressource = validated_data.get('id',instance.id)
        services_json = validated_data.get('services_json')
        ressource = Ressource.objects.get(id=id_ressource)


        if services_json is not None:
            R_SO.objects.filter(ressource=id_ressource).delete()

            for s in services_json:
                service = ServiceOffered.objects.get(id=s['service_offered'])
                R_SO.objects.create(
                    amount=s['amount'],
                    ressource = ressource,
                    service_offered = service
                )

        instance.save()
        return instance

class R_SOSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(read_only=True, source="service_offered.name")
    service_type =serializers.SerializerMethodField(read_only=True, source="service_offered.type")
    service_profit = serializers.CharField(read_only=True, source="service_offered.profit")
    service_area = serializers.CharField(read_only=True, source="service_offered.area.name")
    scale_max_value = serializers.IntegerField(read_only=True, source="service_offered.scale.max_value")
    criticality = serializers.IntegerField(read_only = True, source="service_offered.criticality")
    service_id = serializers.IntegerField(read_only = True,source="service_offered.id")
    
    class Meta:
        model = R_SO
        fields = [
            'id',
            'amount',
            'service_name',
            'service_type',
            'service_profit',
            'service_area',
            'scale_max_value',
            'criticality',
            'service_id'

        ]

    def get_service_type(self,obj):
        return dict(ServiceOffered.TYPE).get(obj.service_offered.type)

    


class Ressources_R_SOSerializer(serializers.ModelSerializer):
    ressource_name = serializers.CharField(read_only=True, source="ressource.name")
    ressource_description = serializers.CharField(read_only=True, source="ressource.description")
    ressource_amount = serializers.CharField(read_only=True, source="ressource.amount")

    class Meta:
        model = R_SO
        fields = [
            'id',
            'amount',
            'ressource_name',
            'ressource_description',
            'ressource_amount',
        ]


class ServiceOfferedStaffRessourceSerializer(serializers.ModelSerializer):
    type_name = serializers.SerializerMethodField(read_only=True)
    area_name = serializers.CharField(read_only=True, source="area.name")
    # Serializer aninado
    staffs_service = SO_SSerializer(many=True, read_only=True, source="service_offered_so_s")
    ressources_service = Ressources_R_SOSerializer(many=True, read_only=True, source="service_offered_r_so")
    # Serializer aninado
    service_offered_service_used = ServiceUsedListSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceOffered
        fields = [
            'id',
            'name',
            'type_name',
            'profit',
            'recovery_time',
            'recovery_point',
            'maximum_recovery_time',
            'criticality',
            'area_name',
            'staffs_service',
            'ressources_service',
            'service_offered_service_used'
        ]

    def get_type_name(self, obj):
        return dict(ServiceOffered.TYPE).get(obj.type)