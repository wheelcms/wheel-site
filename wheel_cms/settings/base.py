import os
from wheelcms_project.settings.base import *

ALLOW_SIGNUP = False

MIDDLEWARE_CLASSES = (
   'django.middleware.locale.LocaleMiddleware',
) + MIDDLEWARE_CLASSES

INSTALLED_APPS = (
    'wheel_cms',
    'wheelcms_carousel',
    'wheelsite_site',
    'wheelcms_valve',
    'wheelcms_disqus',
    'wheelcms_rss',
) + INSTALLED_APPS

MEDIA_ROOT=os.path.join(os.path.dirname(__file__), "..", "..", 'media')
LANGUAGES = (('en', 'English'), ('nl', 'Nederlands'))
CONTENT_LANGUAGES = LANGUAGES
FALLBACK = 'en'
LANGUAGE_CODE = 'en'

