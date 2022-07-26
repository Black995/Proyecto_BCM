from telnetlib import STATUS
from typing import OrderedDict
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        Group, PermissionsMixin)
from django.contrib.auth.password_validation import \
    validate_password as django_validate_password
from django.core.exceptions import ValidationError
from bcm_phase2.models import Staff
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from django.utils.translation import ugettext_lazy as _

class UserManager(BaseUserManager):

    def create_user(self, email, password):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            password=password,
        )

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        if not email:
            raise ValueError('Super Users must have an email address')

        user = self.create_user(
            email=self.normalize_email(email),
            is_superuser=True,
            password=password,
        )

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    
    cleaned_data = {}

    email = models.EmailField(unique=True)
    staff = models.OneToOneField(
        Staff, null=True, related_name='user_staff', on_delete=models.SET_NULL)

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

    
    def validate_password(self, password: str):
        try:
            django_validate_password(password, self)
        except ValidationError as e:
            raise ValidationError({'password': e.messages})

    def save(self, update_fields: list=[], **kwargs):
        #if self.email:
        if self.pk is None or 'email' in update_fields:
            print('email')
            self.email = UserManager.normalize_email(self.email)
        #if self.password:
        if self.pk is None or 'password' in update_fields:
            print('password')
            self.validate_password(self.password)
            self.set_password(self.password)
        
        if not self.is_active:
            self.groups.clear()
        
        super().save(**kwargs)

    def change_password(self, old_password: str, new_password: str):
        if not self.check_password(old_password):
            raise ValidationError({'old_password': _('La contraseña actual es incorrecta')})
        self.password = new_password
        self.save(update_fields=['password'])


