from django_auth_ldap.backend import LDAPBackend
from django.contrib.auth import get_user_model


UserModel = get_user_model()

class CustomLDAPBackend(LDAPBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        return super().authenticate(request, username, password, **kwargs)

