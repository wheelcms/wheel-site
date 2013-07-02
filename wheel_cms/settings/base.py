from wheelcms_project.settings.base import *

ALLOW_SIGNUP = False

INSTALLED_APPS = (
    'wheel_cms',
    'wheelcms_carousel',
    'wheelsite_site',
    'wheelcms_valve',
) + INSTALLED_APPS
