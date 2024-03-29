from django.db import models
from configuration.models import Headquarter, Area, Scale, Position
from bcm_phase1.models import Risk



class Staff(models.Model):
    staff_number = models.CharField(max_length=30, unique=True)
    names = models.CharField(max_length=100)
    surnames = models.CharField(max_length=100)
    earnings = models.FloatField(default=0)
    phone_number_1 = models.CharField(max_length=20)
    phone_number_code_1 = models.CharField(max_length=5)
    phone_number_1_format_international = models.CharField(max_length=20)
    phone_number_2 = models.CharField(max_length=20, null=True, blank=True)
    phone_number_code_2 = models.CharField(max_length=5, null=True, blank=True)
    phone_number_2_format_international = models.CharField(max_length=20, null=True, blank=True)

    headquarter = models.ForeignKey(Headquarter, related_name='headquarter_staff', null=True,
                                    on_delete=models.SET_NULL)
    area = models.ForeignKey(Area, related_name='area_staff', null=True,
                             on_delete=models.SET_NULL)
    position = models.ForeignKey(
        Position, related_name='position_staff', on_delete=models.CASCADE)


class ServiceOffered(models.Model):

    PRODUCT = 1
    SERVICE = 2
    PROCESS = 3
    TYPE = (
        (PRODUCT, 'Producto'),
        (SERVICE, 'Servicio'),
        (PROCESS, 'Proceso'),
    )

    name = models.CharField(max_length=100, unique=True)
    type = models.SmallIntegerField(choices=TYPE)
    profit = models.FloatField()
    recovery_time = models.DurationField()
    criticality = models.SmallIntegerField(null=True, blank=True)
    recovery_point = models.DurationField(null=True, blank=True)
    maximum_recovery_time = models.DurationField(null=True, blank=True)

    area = models.ForeignKey(Area, related_name='area_service_offered', null=True,
                             on_delete=models.SET_NULL)
    scale = models.ForeignKey(Scale, null=True, related_name='scale_service_offered',
                              on_delete=models.SET_NULL)
    headquarters = models.ManyToManyField(
        Headquarter, related_name='headquarter_service_offered')
    _risks = models.ManyToManyField(
        Risk, related_name='risk_service_offered')

    @property
    def risks(self):
        return self._risks.values_list(flat=True)

    @risks.setter
    def risks(self, risks_ids):
        # Eliminamos los registros anteriores de los riesgos
        self._risks.clear()
        # Guardamos los nuevos registros
        if(risks_ids):
            for risk_id in risks_ids:
                risk = Risk.objects.filter(id=risk_id).first()
                if(risk is not None):
                    self._risks.add(risk)




class SO_S(models.Model):

    relevant = models.BooleanField(default=False)
    
    staff = models.ForeignKey(Staff, related_name='staff_so_s',
                             on_delete=models.CASCADE)
    service_offered = models.ForeignKey(ServiceOffered, related_name='service_offered_so_s',
                              on_delete=models.CASCADE)


class ServiceUsed(models.Model):
    
    HIRED = 1
    INTERNAL = 2
    TYPE = (
        (HIRED, 'Contratado'),
        (INTERNAL, 'Interno'),
    )

    name = models.CharField(max_length=100, unique=True)
    type = models.SmallIntegerField(choices=TYPE)
    spending = models.FloatField()
    criticality = models.SmallIntegerField(null=True)
    agreement_comment = models.CharField(max_length=300)

    scale = models.ForeignKey(
        Scale, null=True, related_name='scale_service_used', on_delete=models.SET_NULL)
    headquarters = models.ManyToManyField(
        Headquarter, related_name='headquarter_service_used')
    _services_offered = models.ManyToManyField(
        ServiceOffered, related_name='service_offered_service_used')
    _risks = models.ManyToManyField(
        Risk, related_name='risk_service_used')

    @property
    def services_offered(self):
        return self._services_offered.values_list(flat=True)

    @services_offered.setter
    def services_offered(self, services_offered_ids):
        # Eliminamos los registros anteriores de los servicios ofrecidos
        self._services_offered.clear()
        # Guardamos los nuevos registros
        if(services_offered_ids):
            for service_id in services_offered_ids:
                service = ServiceOffered.objects.filter(id=service_id).first()
                if(service is not None):
                    self._services_offered.add(service)

    @property
    def risks(self):
        return self._risks.values_list(flat=True)

    @risks.setter
    def risks(self, risks_ids):
        # Eliminamos los registros anteriores de los riesgos
        self._risks.clear()
        # Guardamos los nuevos registros
        if(risks_ids):
            for risk_id in risks_ids:
                risk = Risk.objects.filter(id=risk_id).first()
                if(risk is not None):
                    self._risks.add(risk)


class InterestedParty(models.Model):

    SUPPLIER = 1
    INVESTOR = 2
    CUSTOMER = 3
    STAKEHOLDER = 4
    TYPE = (
        (SUPPLIER, 'Proveedor'),
        (INVESTOR, 'Inversionista'),
        (CUSTOMER, 'Cliente'),
        (STAKEHOLDER, 'Accionista'),
    )

    name = models.CharField(max_length=100, unique=True)
    type = models.SmallIntegerField(choices=TYPE)
    description = models.CharField(max_length=200)
    _services_offered = models.ManyToManyField(
        ServiceOffered, related_name='service_offered_interested_party')
    _services_used = models.ManyToManyField(
        ServiceUsed, related_name='service_used_interested_party')

    @property
    def services_offered(self):
        return self._services_offered.values_list(flat=True)
    
    @property
    def services_used(self):
        return self._services_used.values_list(flat=True)

    @services_offered.setter
    def services_offered(self, services_offered_ids):
        # Eliminamos los registros anteriores de los servicios ofrecidos
        self._services_offered.clear()
        # Guardamos los nuevos registros
        if(services_offered_ids):
            for service_id in services_offered_ids:
                service = ServiceOffered.objects.filter(id=service_id).first()
                if(service is not None):
                    self._services_offered.add(service)

    @services_used.setter
    def services_used(self,services_used_ids):
            self._services_used.clear()
            if(services_used_ids):
                for service_id in services_used_ids:
                    service = ServiceUsed.objects.filter(id=service_id).first()
                    if(service is not None):
                        self._services_used.add(service) 






class OrganizationActivity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200)
    cost = models.FloatField()
    recovery_time = models.DurationField()
    criticality = models.SmallIntegerField(null=True, blank=True)

    _services_offered = models.ManyToManyField(
        ServiceOffered, related_name='service_offered_organizacion_activity')
    scale = models.ForeignKey(
        Scale, null=True, related_name='scale_organization_activity', on_delete=models.SET_NULL)
    _headquarters = models.ManyToManyField(
        Headquarter, related_name='headquarter_organization_activity')
    _risks = models.ManyToManyField(
        Risk, related_name='risk_organizacion_activity')
    

    @property
    def risks(self):
        return self._risks.values_list(flat=True)

    @risks.setter
    def risks(self, risks_ids):
        # Eliminamos los registros anteriores de los riesgos
        self._risks.clear()
        # Guardamos los nuevos registros
        if(risks_ids):
            for risk_id in risks_ids:
                risk = Risk.objects.filter(id=risk_id).first()
                if(risk is not None):
                    self._risks.add(risk)
    
    @property
    def services_offered(self):
        return self._services_offered.values_list(flat=True)

    @services_offered.setter
    def services_offered(self, services_offered_ids):

        print(services_offered_ids)
        # Eliminamos los registros anteriores de los servicios ofrecidos
        self._services_offered.clear()
        # Guardamos los nuevos registros
        if(services_offered_ids):
            for service_id in services_offered_ids:
                print(service_id)
                service = ServiceOffered.objects.filter(id=service_id).first()
                if(service is not None):
                    self._services_offered.add(service)
    



class Ressource(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    amount = models.PositiveIntegerField(default=0)


class R_SO(models.Model):
    amount = models.PositiveIntegerField(default=0)
    ressource = models.ForeignKey(
        Ressource, related_name='ressource_r_so', on_delete=models.CASCADE)
    service_offered = models.ForeignKey(
        ServiceOffered, related_name='service_offered_r_so', on_delete=models.CASCADE)
