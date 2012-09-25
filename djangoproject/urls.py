from django.contrib import admin
from django.conf.urls.defaults import patterns, include, url

from django.conf import settings

import two.userauth.login
import two.userauth.signup

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = staticfiles_urlpatterns()

## or import static_urls; urlpatterns = static_urls.urlpatterns

urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

