from settings.base import *
from settings.base.util import get_env_variable

PG_DEFAULT_DB = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable('DB_NAME'),
        'USER': get_env_variable('DB_USER'),
        'PASSWORD': get_env_variable('DB_PASSWORD'),
        'HOST': get_env_variable('DB_HOST', 'localhost'),
        'PORT': get_env_variable('DB_PORT', ''),
}

DATABASES = {
        'default': PG_DEFAULT_DB
}

STATIC_ROOT = get_env_variable('PROJECT_HOME') + '/staticfiles'
MEDIA_ROOT = get_env_variable('PROJECT_HOME') + '/media'
DEBUG=False

STRACKS_URL = get_env_variable('STRACKS_URL', '')

STRACKS_CONNECTOR = None

if STRACKS_URL:
    from stracks_api.connector import ASyncHTTPConnector
    STRACKS_CONNECTOR = ASyncHTTPConnector(STRACKS_URL)
    MIDDLEWARE_CLASSES += (
        'stracks_api.middleware.StracksMiddleware',
    )
