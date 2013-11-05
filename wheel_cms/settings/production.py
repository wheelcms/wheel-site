from settings.base import *
from wheelcms_project.settings.base.util import get_env_variable

DEBUG=False

STRACKS_URL = get_env_variable('STRACKS_URL', '')

STRACKS_CONNECTOR = None

if STRACKS_URL:
    from stracks_api.connector import ASyncHTTPConnector
    STRACKS_CONNECTOR = ASyncHTTPConnector(STRACKS_URL)
    MIDDLEWARE_CLASSES += (
        'stracks_api.middleware.StracksMiddleware',
    )
