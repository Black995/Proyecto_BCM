from django.contrib import admin
from .import models

# Register your models here.
admin.site.register(models.Organization)
admin.site.register(models.Headquarter)
admin.site.register(models.Position)
admin.site.register(models.Area)
admin.site.register(models.Scale)
admin.site.register(models.ScaleView)
admin.site.register(models.State)
admin.site.register(models.City)
admin.site.register(models.Township)
admin.site.register(models.Parish)

# Deben ocultarse estos modelos cuando el sistema esté en producción
admin.site.register(models.ProductActivation)
admin.site.register(models.UsedKeys)
