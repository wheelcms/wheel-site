from settings_admin import *
from settings_locale import *
from settings_paths import *
from settings_django import *
from settings_logging import *
# from settings_mail import *
from settings_database import *

from wheelcms_axle.settings import *

try:
    from local_settings import *
except ImportError:
    pass

import sys

if 'ptest' in sys.argv or 'test' in sys.argv:
    DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'memory:///'
        }
    }

## verify required stuff has been set
if not SECRET_KEY:
    raise RuntimeError("Configure the SECRET_KEY in settings_django")

