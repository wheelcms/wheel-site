from django.conf.urls.defaults import patterns, url

from django.conf import settings
import re
prefix = settings.STATIC_URL

## In non-dev mode requires --insecure to work
urlpatterns = patterns('',
        url(r'^%s(?P<path>.*)$' % re.escape(prefix.lstrip('/')), 
            "django.contrib.staticfiles.views.serve"),
    )


