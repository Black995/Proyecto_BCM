from django.db import models
from users.models import User




class Organization(models.Model):
    name = models.CharField(max_length=150, unique=True)
    legal_id = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=350)
    logo = models.ImageField(
        upload_to='organization_logo', null=True, blank=True)



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

