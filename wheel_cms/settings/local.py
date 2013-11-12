from settings.base import *

from wheelcms_project.settings.base.util import get_env_variable

SITE_ID = 1
# local mail config

ADMINS = ( ( "Ivo", "test-wheel@in.m3r.nl"),  )

DEBUG = True


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# INSTALLED_APPS += ('debug_toolbar', )
# INTERNAL_IPS = ('127.0.0.1',)
# MIDDLEWARE_CLASSES += \
# ('debug_toolbar.middleware.DebugToolbarMiddleware', )
# 

LANGUAGES = (('en', 'English'), ('nl', 'Nederlands'))
# LANGUAGES = (('en', 'English'), )
CONTENT_LANGUAGES = LANGUAGES

STRACKS_URL = get_env_variable('STRACKS_URL', '')

STRACKS_CONNECTOR = None

if STRACKS_URL:
    from stracks_api.connector import HTTPConnector
    STRACKS_CONNECTOR = HTTPConnector(STRACKS_URL)
    MIDDLEWARE_CLASSES += (
        'stracks_api.middleware.StracksMiddleware',
    )
