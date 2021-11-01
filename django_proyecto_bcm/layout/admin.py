from django.contrib import admin
from .import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Organization)
admin.site.register(models.InterestedParty)
admin.site.register(models.Location)
admin.site.register(models.Headquarter)
admin.site.register(models.Position)
admin.site.register(models.Area)
admin.site.register(models.Staff)
admin.site.register(models.Scale)
admin.site.register(models.ScaleView)
admin.site.register(models.ServiceOffered)
admin.site.register(models.ServiceUsed)
admin.site.register(models.OrganizationActivity)
admin.site.register(models.Risk)
admin.site.register(models.CrisisScenario)
admin.site.register(models.IncidentHistory)
