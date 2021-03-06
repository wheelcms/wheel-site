from .base import *

INSTALLED_APPS += ("wheelcms_axle.tests", "wheelcms_valve")

TEST_DB = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'memory:///'
}

#CONTENT_LANGUAGES = ('any',)
#FALLBACK = 'any'

DATABASES = {
    'default': TEST_DB
}

TEST_MEDIA_ROOT = "/tmp/wheel-cms-test-media"
CLEANUP_MEDIA = True

HAYSTACK_CONNECTIONS={'default':{'engine':'haystack.backends.simple_backend.SimpleEngine'}}

CONTENT_LANGUAGES=(('en', 'English'), ('nl', 'Nederlands'))
FALLBACK='en'
LANGUAGE_CODE='en'
