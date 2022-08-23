from django.db import models
import os
from django.conf import settings


def ruta_archivo_org(instance, filename):    
    return os.path.join(settings.STATICFILES_DIRS[0], str(instance.name), str(instance.name) + str(os.path.splitext(filename)[1]))

class Organization(models.Model):
    name = models.CharField(max_length=150, unique=True)
    legal_id = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=350)
    logo = models.ImageField(
        upload_to=ruta_archivo_org, null=True, blank=True, max_length=1000000)


class State(models.Model):

    name = models.CharField(max_length=100, unique=True)
    iso_3166_2 = models.CharField(max_length=5)
    

class City(models.Model):

    CAPITAL = 1
    NON_CAPITAL = 0
    TYPE = (
        (CAPITAL, 'Capital'),
        (NON_CAPITAL, 'No es capital')
    )

    name = models.CharField(max_length=100)
    capital = models.SmallIntegerField(choices=TYPE)
    state = models.ForeignKey(
        State, related_name='state_city', on_delete=models.CASCADE)
    

class Township(models.Model):

    name = models.CharField(max_length=100)
    state = models.ForeignKey(
        State, related_name='state_twonship', on_delete=models.CASCADE)
        

class Parish(models.Model):

    name = models.CharField(max_length=100)
    township = models.ForeignKey(
        Township, related_name='township_parish', on_delete=models.CASCADE)





class Headquarter(models.Model):
    name = models.CharField(max_length=100, unique=True)

    city = models.ForeignKey(
        City, related_name='city_headquarter', null=True, on_delete=models.SET_NULL)
    parish = models.ForeignKey(
        Parish, related_name='parish_headquarter', null=True, on_delete=models.SET_NULL)


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
    minimum_recovery_time = models.DurationField(blank=True, null=True)
    minimum_scale_value = models.SmallIntegerField(blank=True, null=True)

