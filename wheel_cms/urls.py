from django.conf.urls import *
from django.conf.urls.i18n import i18n_patterns

from wheelcms_project.urls import handler500, handler404, basepatterns, wheelpatterns

urlpatterns = i18n_patterns('',
    (r'', include(wheelpatterns)),
) + patterns('',
#    (r'^captcha/', include('captcha.urls')),
    (r'', include(basepatterns)),
)

