from django.db import models
from configuration.models import Organization, Headquarter, Area


class InterestedParty(models.Model):

    SUPPLIER = 1
    INVESTOR = 2
    CUSTOMER = 3
    STAKEHOLDER = 3
    TYPE = (
        (SUPPLIER, 'Proveedor'),
        (INVESTOR, 'Inversionista'),
        (CUSTOMER, 'Cliente'),
        (STAKEHOLDER, 'Accionista'),
    )

    name = models.CharField(max_length=100, unique=True)
    type = models.SmallIntegerField(choices=TYPE)
    description = models.CharField(max_length=200)

    organization = models.ForeignKey(
        Organization, related_name='organization_interested_party', on_delete=models.CASCADE)


class Scale(models.Model):
    name = models.CharField(max_length=100, unique=True)
    min_value = models.SmallIntegerField()
    max_value = models.SmallIntegerField()


"""
    This model is used for restrict the use of a scale in front-end views
"""


class ScaleView(models.Model):
    name = models.CharField(max_length=100, unique=True)

    scale = models.ForeignKey(
        Scale, related_name='scale_view', on_delete=models.CASCADE)


class ServiceOffered(models.Model):

    PRODUCT = 1
    SERVICE = 2
    TYPE = (
        (PRODUCT, 'Producto'),
        (SERVICE, 'Servicio'),
    )

    name = models.CharField(max_length=100, unique=True)
    type = models.SmallIntegerField(choices=TYPE)
    profit = models.FloatField()
    # frecuency =
    recovery_time = models.DurationField()
    criticality = models.SmallIntegerField(null=True)

    area = models.ForeignKey(Area, related_name='area_service_offered', null=True,
                             on_delete=models.SET_NULL)
    scale = models.OneToOneField(
        Scale, null=True, related_name='scale_service_offered', on_delete=models.SET_NULL)
    headquarters = models.ManyToManyField(
        Headquarter, related_name='headquarter_service_offered')


class ServiceUsed(models.Model):
    name = models.CharField(max_length=100, unique=True)
    spending = models.FloatField()
    # frecuency =
    recovery_time = models.DurationField()
    criticality = models.SmallIntegerField(null=True)

    services_offered = models.ManyToManyField(
        ServiceOffered, related_name='service_offered_service_offered')
    scale = models.OneToOneField(
        Scale, null=True, related_name='scale_service_used', on_delete=models.SET_NULL)
    headquarters = models.ManyToManyField(
        Headquarter, related_name='headquarter_service_used')


class OrganizationActivity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200)
    cost = models.FloatField()
    # frecuency =
    recovery_time = models.DurationField()
    criticality = models.SmallIntegerField(null=True)

    services_offered = models.ManyToManyField(
        ServiceOffered, related_name='service_offered_organizacion_activity')
    scale = models.OneToOneField(
        Scale, null=True, related_name='scale_organization_activity', on_delete=models.SET_NULL)
    headquarters = models.ManyToManyField(
        Headquarter, related_name='headquarter_organization_activity')

