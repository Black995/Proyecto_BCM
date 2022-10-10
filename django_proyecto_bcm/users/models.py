import os
import re
from telnetlib import STATUS
from typing import OrderedDict
from uuid import uuid4
from django.db import models
from django.conf import settings as api_settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        Group, PermissionsMixin)
from django.contrib.auth.password_validation import \
    validate_password as django_validate_password
from django.core.exceptions import ValidationError
from bcm_phase2.models import Staff
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.utils.translation import ugettext_lazy as _
from configuration.models import Organization
from django.template.loader import get_template
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives, get_connection



"""
    Función para enviar correos
"""
def send_mail(subject, message, from_email, recipient_list,
              fail_silently=False, auth_user=None, auth_password=None,
              connection=None, html_message=None, image_path=''):
    """
    Override send_mail from django.core.mail.send_mail for allow image in email and get default email credentials
    """
    host = api_settings.EMAIL_HOST
    port = api_settings.EMAIL_PORT
    auth_user = auth_user or api_settings.EMAIL_HOST_USER
    auth_password = auth_password or api_settings.EMAIL_HOST_PASSWORD
    from_email = from_email or api_settings.EMAIL_HOST_USER

    connection = connection or get_connection(
        host=host,
        port=port,
        username=auth_user,
        password=auth_password,
        fail_silently=fail_silently,
    )
    mail = EmailMultiAlternatives(
        subject, message, from_email, recipient_list, connection=connection)
    if html_message:
        mail.attach_alternative(html_message, 'text/html')

    """
    if image_path:
        try:
            with open(image_path, mode='rb') as f:
                image = MIMEImage(f.read())
                mail.attach(image)
                image.add_header(
                    'Content-ID', f"<{os.path.basename(image_path)}>")
        except FileNotFoundError:
            pass
    """

    return mail.send()

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
    
    password_reset_token_datetime = models.DateTimeField(null=True)
    password_reset_token = models.CharField(max_length=32, null=True)

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
            raise ValidationError({'old_password': _('old password')})
        self.password = new_password
        self.save(update_fields=['password'])
    
    def generate_password_reset_token(self):
        self.password_reset_token = uuid4().hex
        self.password_reset_token_datetime = timezone.now()
        self.save(update_fields=['password_reset_token',
                  'password_reset_token_datetime'])
    
    def send_password_reset_email(self):
        # Organization information
        org = Organization.objects.all().first()
        # Generating token
        self.generate_password_reset_token()
        # Building template context
        subject = _('Password reset')
        # Getting logo
        organization_logo_path = org.logo.path if bool(
            org.logo) else ''
        organization_logo_filename = os.path.basename(organization_logo_path)
        ctx = {
            'organization_logo_filename': organization_logo_filename,
            'greeting_message': _('Hola {user_name},').format(user_name=self.staff.names + " " + self.staff.surnames),
            'message': _('Usted ha solicitado recuperar su contraseña para su cuenta. Por favor dirígase al siguiente link {password_reset_link} para recuperar su contraseña.').
            format(password_reset_link=api_settings.PASSWORD_RESET_LINK.format(token=self.password_reset_token)),
            'farewell_message': _('Saludos, \n\n{organization_name}.').format(organization_name=org.name),
        }
        # Rendering context into template
        message = get_template('password_reset.html').render(ctx)
        # Sending email
        send_mail(subject=subject, message='', from_email=api_settings.EMAIL_HOST_USER,
                  recipient_list=[self.email], fail_silently=False, html_message=message, image_path=organization_logo_path)


    def invalidate_password_reset_token(self, save: bool = True):
        if self.password_reset_token is not None:
            self.password_reset_token = None
            self.password_reset_token_datetime = None
            if save:
                self.save(update_fields=['password_reset_token',
                                         'password_reset_token_datetime'])

    def is_the_password_reset_token_active(self):
        # Tiempo de duración del token = 3 horas
        return self.password_reset_token_datetime is not None \
            and timezone.now() < self.password_reset_token_datetime + timedelta(hours=3)

    @staticmethod
    def reset_password(token, password):
        user = User.objects.filter(password_reset_token=token).first()
        if user is not None and user.is_the_password_reset_token_active():
            user.password = password
            user.invalidate_password_reset_token(save=False)
            user.save(update_fields=['password', 'password_reset_token',
                                     'password_reset_token_datetime'])



