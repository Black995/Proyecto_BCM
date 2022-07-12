import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _
from settings.models import Settings

User = get_user_model()


@deconstructible
class UserRoleValidator:
    code = 'invalid_user_role'

    def __init__(self, *roles, user_roles_allowed_for_risk_responsible: bool = False):
        self.roles = roles
        self.user_roles_allowed_for_risk_responsible = user_roles_allowed_for_risk_responsible

    def __call__(self, value):
        user = None
        if isinstance(value, int):
            user = User.objects.filter(pk=value).first()
        elif isinstance(value, User):
            user = value
        if self.user_roles_allowed_for_risk_responsible:
            self.roles = Settings.get_settings().user_roles_allowed_for_risk_responsible
        if not user.has_role(*self.roles):
            raise ValidationError(
                message=_('The user must have one of the following roles {roles}.').format(
                    roles=[dict(User.ROLES).get(role) for role in self.roles]),
                code=self.code,
            )


class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall('\d', password):
            raise ValidationError(
                _("The password must contain at least 1 digit, 0-9."),
                code='password_no_number',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 digit, 0-9."
        )


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("The password must contain at least 1 uppercase letter, A-Z."),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 uppercase letter, A-Z."
        )


class LowercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError(
                _("The password must contain at least 1 lowercase letter, a-z."),
                code='password_no_lower',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 lowercase letter, a-z."
        )


class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                _("The password must contain at least 1 symbol: " +
                  "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 symbol: " +
            "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
        )
