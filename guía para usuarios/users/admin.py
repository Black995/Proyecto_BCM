from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from erm_api.admin import EntityAdmin

User = get_user_model()

admin.site.register([Permission, ])
admin.site.register([User, ], EntityAdmin)
