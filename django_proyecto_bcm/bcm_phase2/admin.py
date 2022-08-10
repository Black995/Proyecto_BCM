from django.contrib import admin
from .import models

# Register your models here.
admin.site.register(models.InterestedParty)
admin.site.register(models.ServiceOffered)
admin.site.register(models.ServiceUsed)
admin.site.register(models.OrganizationActivity)
admin.site.register(models.Staff)
admin.site.register(models.SO_S)