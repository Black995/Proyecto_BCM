import os
import re
from datetime import timedelta
from uuid import uuid4

from django.apps import apps
from django.conf import settings as api_settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        Group, PermissionsMixin)
from django.contrib.auth.password_validation import \
    validate_password as django_validate_password
from django.core.exceptions import ValidationError
from django.db import models
from django.template.loader import get_template
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from erm_api.models import Entity, EntityManager
from erm_api.utils import send_mail


def get_settings():
    from settings.models import Settings
    return Settings.get_settings()


class UserManager(EntityManager, BaseUserManager):

    def create_superuser(self, **kwargs):
        kwargs['role'] = User.ADMINISTRATOR
        u = User(**kwargs)
        return u.save(update_fields=kwargs.keys())


class User(Entity, AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    MEMBER_BOARD_DIRECTORS = 1
    GENERAL_MANAGER = 2
    AREA_MANAGER = 3
    AREA_ERM_MANAGER = 4
    AREA_SPECIALIST = 5
    AREA_ANALYST = 6
    INTERNAL_AUDITOR = 7
    SECURITY_AND_SYSTEMS = 8
    ADMINISTRATOR = 9
    UNKNOWN = 10
    ROLES = (
        (UNKNOWN, _('Unknown')),
        (MEMBER_BOARD_DIRECTORS, _('Member of the Board of Directors')),
        (GENERAL_MANAGER, _('President/General Manager/Senior Management')),
        (AREA_MANAGER, _('Vice President/Area Manager')),
        (AREA_ERM_MANAGER, _('Area ERM Manager')),
        (AREA_SPECIALIST, _('Area Specialist')),
        (AREA_ANALYST, _('Area Analyst')),
        (INTERNAL_AUDITOR, _('Internal Auditor')),
        (SECURITY_AND_SYSTEMS, _('Security and Systems')),
        (ADMINISTRATOR, _('Administrator')),
    )

    GROUPS_CODENAME = (
        (UNKNOWN, _('UNKNOWN')),
        (MEMBER_BOARD_DIRECTORS, 'MEMBER_BOARD_DIRECTORS'),
        (GENERAL_MANAGER, 'GENERAL_MANAGER'),
        (AREA_MANAGER, 'AREA_MANAGER'),
        (AREA_ERM_MANAGER, 'AREA_ERM_MANAGER'),
        (AREA_SPECIALIST, 'AREA_SPECIALIST'),
        (AREA_ANALYST, 'AREA_ANALYST'),
        (INTERNAL_AUDITOR, 'INTERNAL_AUDITOR'),
        (SECURITY_AND_SYSTEMS, 'SECURITY_AND_SYSTEMS'),
    )

    email = models.EmailField(
        max_length=50, unique=True, verbose_name=_('email'))
    first_name = models.CharField(max_length=50, verbose_name=_('first name'))
    second_name = models.CharField(
        max_length=50, default='', blank=True, verbose_name=_('second name'))
    last_name = models.CharField(max_length=50, verbose_name=_('last name'))
    second_last_name = models.CharField(
        max_length=50, default='', blank=True, verbose_name=_('second last name'))
    role = models.PositiveSmallIntegerField(
        default=UNKNOWN, choices=ROLES, verbose_name=_('role'))
    is_substitute = models.BooleanField(
        default=False, verbose_name=_('substitute'))
    is_superuser = models.BooleanField(
        default=False, verbose_name=_('superuser'))
    password_reset_token_datetime = models.DateTimeField(
        null=True, verbose_name=_('password reset token date'))
    password_reset_token = models.CharField(
        max_length=32, null=True, verbose_name=_('password reset token'))

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'second_name',
                       'last_name', 'second_last_name', ]

    @property
    def is_staff(self):
        # All superusers are staff
        return self.is_superuser

    @property
    def name(self):
        name = f'{self.first_name} {self.second_name} {self.last_name} {self.second_last_name}'
        name = name.strip()
        name = re.sub(' +', ' ', name)
        return name

    @property
    def role_name(self):
        return dict(self.ROLES).get(self.role)

    @property
    def areas(self) -> 'list[int]':
        if self.has_role(self.AREA_MANAGER):
            return [self.area_manager.pk] if getattr(self, 'area_manager', None) is not None else []
        elif self.has_role(self.AREA_ERM_MANAGER):
            return [self.area_erm_manager.pk] if getattr(self, 'area_erm_manager', None) is not None else []
        if self.has_role(self.AREA_SPECIALIST, self.AREA_ANALYST):
            return self._areas.values_list('pk', flat=True)
        else:
            Area = apps.get_model('government', 'area')
            return Area.objects.all_with_deleted().values_list('pk', flat=True)

    @property
    def count_unread_notifications(self):
        return self.notifications.filter(read__isnull=True).count()

    def save(self, update_fields: list = [], **kwargs):
        changed_fields = self.changed_fields
        # Normalizing email
        if self.pk is None or 'email' in changed_fields:
            self.email = BaseUserManager.normalize_email(self.email)
        # Marking admin user as superuser
        set_group = self.pk is None or 'role' in changed_fields
        if set_group:
            self.is_superuser = self.role is User.ADMINISTRATOR
        # Encrypting password
        if self.pk is None or 'password' in changed_fields:
            self.validate_password(self.password)
            self.set_password(self.password)
        super().save(**kwargs)
        # Assigning group according to role
        if set_group:
            self.groups.clear()
            if self.role is not User.ADMINISTRATOR:
                group = Group.objects.filter(
                    name=dict(self.GROUPS_CODENAME).get(self.role)).first()
                if group is not None:
                    self.groups.add(group)

    def has_role(self, *roles) -> bool:
        return self.role in roles

    def validate_password(self, password: str):
        try:
            django_validate_password(password, self)
        except ValidationError as e:
            raise ValidationError({'password': e.messages})

    def change_password(self, old_password: str, new_password: str):
        if not self.check_password(old_password):
            raise ValidationError({'old_password': _('Wrong password')})
        self.password = new_password
        self.save(update_fields=['password'])

    def generate_password_reset_token(self):
        self.password_reset_token = uuid4().hex
        self.password_reset_token_datetime = timezone.now()
        self.save(update_fields=['password_reset_token',
                  'password_reset_token_datetime'])

    def invalidate_password_reset_token(self, save: bool = True):
        if self.password_reset_token is not None:
            self.password_reset_token = None
            self.password_reset_token_datetime = None
            if save:
                self.save(update_fields=['password_reset_token',
                                         'password_reset_token_datetime'])

    def send_password_reset_email(self):
        # Getting settings
        settings = get_settings()
        # Generating token
        self.generate_password_reset_token()
        # Building template context
        subject = _('Password reset')
        # Getting logo
        organization_logo_path = settings.organization_logo.path if bool(
            settings.organization_logo) else ''
        organization_logo_filename = os.path.basename(organization_logo_path)
        ctx = {
            'organization_logo_filename': organization_logo_filename,
            'greeting_message': _('Hello {user_name},').format(user_name=self.first_name),
            'message': _('You have requested a password reset for your account. Please click the link {password_reset_link} to reset your password.').
            format(password_reset_link=settings.get_password_reset_link(
                self.password_reset_token)),
            'farewell_message': _('Best regards, \n\n{organization_name}.').format(organization_name=settings.organization_name),
        }
        # Rendering context into template
        message = get_template('password_reset.html').render(ctx)
        # Sending email
        send_mail(subject=subject, message='', from_email=api_settings.EMAIL_HOST_USER,
                  recipient_list=[self.email], fail_silently=True, html_message=message, image_path=organization_logo_path)

    def is_the_password_reset_token_active(self):
        settings = get_settings()
        return self.password_reset_token_datetime is not None \
            and timezone.now() < self.password_reset_token_datetime + timedelta(hours=settings.password_reset_token_expiration_hours)

    @staticmethod
    def reset_password(token, password):
        user = User.objects.filter(password_reset_token=token).first()
        if user is not None and user.is_the_password_reset_token_active():
            user.password = password
            user.invalidate_password_reset_token(save=False)
            user.save(update_fields=['password', 'password_reset_token',
                                     'password_reset_token_datetime'])
