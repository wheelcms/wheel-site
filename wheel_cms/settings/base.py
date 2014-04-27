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
    'wheelcms_users',
    'drole',
) + INSTALLED_APPS

# LANGUAGES = (('en', 'English'), ('nl', 'Nederlands'))
LANGUAGES = (('en', 'English'), )
CONTENT_LANGUAGES = LANGUAGES
FALLBACK = 'en'
LANGUAGE_CODE = 'en'

