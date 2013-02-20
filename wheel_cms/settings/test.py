from settings.base import *

INSTALLED_APPS += ("wheelcms_axle.tests", )

TEST_DB = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'memory:///'
}


DATABASES = {
    'default': TEST_DB
}
