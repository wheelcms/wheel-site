from settings.base import *
from wheelcms_project.settings.base.util import get_env_variable

if not DATABASE_URL:
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

DEBUG=False

STRACKS_URL = get_env_variable('STRACKS_URL', '')

STRACKS_CONNECTOR = None

if STRACKS_URL:
    from stracks_api.connector import ASyncHTTPConnector
    STRACKS_CONNECTOR = ASyncHTTPConnector(STRACKS_URL)
    MIDDLEWARE_CLASSES += (
        'stracks_api.middleware.StracksMiddleware',
    )
