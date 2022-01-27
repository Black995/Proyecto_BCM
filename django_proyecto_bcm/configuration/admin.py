from django.contrib import admin
from .import models

# Register your models here.
admin.site.register(models.Organization)
admin.site.register(models.Location)
admin.site.register(models.Headquarter)
admin.site.register(models.Position)
admin.site.register(models.Area)
admin.site.register(models.Staff)
