from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):

    def create_user(self, email, password):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        if not email:
            raise ValueError('Super Users must have an email address')

        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )

        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)

    # AbstractBaseUser
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_perms(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    "All organization member is an staff"
    @property
    def is_staff(self):
        return True


class Organization(models.Model):
    name = models.CharField(max_length=150, unique=True)
    legal_id = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=350)
    logo = models.ImageField(
        upload_to='organization_logo', null=True, blank=True)


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


"""
    Recursive relation will be evaluated, depending the final location model use
"""


class Location(models.Model):

    COUNTRY = 1
    STATE = 2
    CITY = 3
    TYPE = (
        (COUNTRY, 'País'),
        (STATE, 'Estado'),
        (CITY, 'Ciudad'),
    )

    name = models.CharField(max_length=100, unique=True)
    type = models.SmallIntegerField(choices=TYPE)
    # uper_location = models.ForeignKey(
    #    'Location', blank=True, null=True, related_name='upper_location', on_delete=models.SET_NULL)


class Headquarter(models.Model):
    name = models.CharField(max_length=100, unique=True)

    location = models.OneToOneField(Location, related_name='location_headquarter', null=True,
                                    on_delete=models.SET_NULL)


class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)
    relevant = models.BooleanField(default=False)


class Area(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Staff(models.Model):
    staff_number = models.IntegerField(null=True)
    names = models.CharField(max_length=100)
    surnames = models.CharField(max_length=100)
    earnings = models.IntegerField()

    user = models.OneToOneField(
        User, null=True, related_name='user_staff', on_delete=models.SET_NULL)
    Headquarter = models.ForeignKey(Headquarter, related_name='headquarter_staff', null=True,
                                    on_delete=models.SET_NULL)
    area = models.ForeignKey(Area, related_name='area_staff', null=True,
                             on_delete=models.SET_NULL)
    position = models.ForeignKey(
        Position, related_name='position_staff', on_delete=models.CASCADE)


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


class Risk(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200)

    services_offered = models.ManyToManyField(
        ServiceUsed, related_name='service_used_risk')
    organizacion_activities = models.ManyToManyField(
        OrganizationActivity, related_name='organizacion_activity_risk')
    headquarters = models.ManyToManyField(
        Headquarter, related_name='headquarter_risk')
    staffs = models.ManyToManyField(
        Staff, related_name='staff_risk')


class CrisisScenario(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200)

    headquarters = models.ManyToManyField(
        Headquarter, related_name='headquarter_crisis_scenario')
    _risks = models.ManyToManyField(
        Risk, related_name='crisis_scenario_risk', db_column='risks')
    
    @property
    def risks(self):
        return self._risks.values_list(flat=True)


class IncidentHistory(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.CharField(max_length=200, null=True, blank=True)

    crisis_scenario = models.ForeignKey(
        CrisisScenario, related_name='crisis_scenario_indicent_history', on_delete=models.CASCADE)
