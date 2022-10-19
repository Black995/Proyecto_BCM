"""
Django settings for django_proyecto_bcm project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from email.policy import default
from pathlib import Path
from celery.schedules import crontab
from django_proyecto_bcm.celery import app
import os
import environ
import datetime

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True),
    BROKER_HOST=(str, '127.0.0.1'),
    BROKER_PORT=(int, 6379),
)
# reading .env file
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$^%w4a)%zbi$(&p9kdb1vimran5&#@(!%24l(f5w3bz0k$3ld!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'django_extensions',
    'users',
    'configuration',
    'bcm_phase1',
    'bcm_phase2',
    'bcm_phase3',
    'notifications',



    'channels',
]

AUTH_USER_MODEL = 'users.User'

"""
    Configuraciones del cors
"""
# CORS_ORIGIN_ALLOW_ALL = True
ALLOWED_HOSTS = ['*']

# If this is used then `CORS_ORIGIN_WHITELIST` will not have any effect
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
""""
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
    'http://localhost:8080',
)
CORS_ALLOW_CREDENTIALS = True
"""

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# Configuration JWT object
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(hours=12),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(hours=12),
}


ROOT_URLCONF = 'django_proyecto_bcm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates', 'email_templates'), 
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_proyecto_bcm.wsgi.application'

ASGI_APPLICATION = 'django_proyecto_bcm.routing.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': env('ENGINE'),
        'NAME': env('NAME'),
        'USER': env('DBUSER'),
        'PASSWORD': env('PASSWORD'),
        'HOST': env('HOST'),
        'PORT': int(env('PORT')),
        'ATOMIC_REQUESTS': True,
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'es-ES'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

#MEDIA_URL = '/media/'
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(MEDIA_ROOT, 'organization'),
    os.path.join(MEDIA_ROOT, 'users'),
    os.path.join(BASE_DIR, 'Ressources'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
    os.path.join(BASE_DIR, 'bcm_phase1', 'locale'),
    os.path.join(BASE_DIR, 'bcm_phase2', 'locale'),
    os.path.join(BASE_DIR, 'bcm_phase3', 'locale'),
    os.path.join(BASE_DIR, 'configuration', 'locale'),
    os.path.join(BASE_DIR, 'users', 'locale'),
    os.path.join(BASE_DIR, 'notifications', 'locale'),
)

EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = int(env('EMAIL_PORT'))
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

PASSWORD_RESET_LINK = env('PASSWORD_RESET_LINK')

### LDAP Settings ###
"""
import ldap
from django_auth_ldap.config import LDAPSearch

if env('AUTH_LDAP'):
    # Baseline configuration.
    AUTH_LDAP_SERVER_URI = env('AUTH_LDAP_SERVER_URI')

    AUTH_LDAP_USER_SEARCH = LDAPSearch(
        env('AUTH_LDAP_USER_SEARCH_BASE_DN'),
        ldap.SCOPE_SUBTREE,
        '(uid=%(user)s)',
    )

    # Populate the Django user from the LDAP directory.
    AUTH_LDAP_USER_ATTR_MAP = {
        'first_name': 'givenName',
        'last_name': 'sn',
        'email': 'mail',
    }

    AUTH_LDAP_ALWAYS_UPDATE_USER = True

    AUTHENTICATION_BACKENDS = (
        'django_proyecto_bcm.authenticators_ldap.CustomLDAPBackend',
        'django.contrib.auth.backends.ModelBackend',
    )
"""

CELERY_BROKER_URL = f'redis://{env("BROKER_HOST")}:{env("BROKER_PORT")}'
app.conf.enable_utc = True
CELERY_BEAT_SCHEDULE = {
    'every-minute':{
        'task': 'configuration.tasks.ExpirationDateVerification',
        'schedule': crontab(minute='0',hour='0'),

    },
    'every-day':{
        'task': 'notifications.tasks.RemainingActivationTimeNotifiaction',
        'schedule': crontab(minute='1',hour="0")
    }
}
