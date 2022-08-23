from django.contrib import admin
from .import models

# Register your models here.
admin.site.register(models.IncidentHistory)
admin.site.register(models.ContingencyPlan)
