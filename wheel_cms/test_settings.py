from settings.base import *

INSTALLED_APPS += ("wheelcms_axle.tests", )

DATABASES = {
    'default': TEST_DB
}
