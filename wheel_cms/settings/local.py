from settings.base import *

from .base.util import get_env_variable

SITE_ID = 1
# local mail config

DEBUG = True

SQLITE_DEFAULT_DB = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'wheel.db',
}

PG_DEFAULT_DB = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'somename',
        'USER': 'someone',  # get_env_variable ...
        'PASSWORD': 'somesecret',  # get_env_variable ...
        'HOST': 'localhost',
        'PORT': '',
}

DATABASES = {
    'default': SQLITE_DEFAULT_DB,
}

MAIL_SENDER = get_env_variable('POSTMARK_SENDER')
POSTMARK_API_KEY = get_env_variable('POSTMARK_API_KEY')
POSTMARK_SENDER = MAIL_SENDER
EMAIL_BACKEND = 'postmark.django_backend.EmailBackend'

DEFAULT_FROM_EMAIL = MAIL_SENDER

# INSTALLED_APPS += ('debug_toolbar', )
# INTERNAL_IPS = ('127.0.0.1',)
# MIDDLEWARE_CLASSES += \
# ('debug_toolbar.middleware.DebugToolbarMiddleware', )
# 
