from settings.base import *

INSTALLED_APPS += ("wheelcms_axle.tests", )

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}
