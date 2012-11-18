from django.conf.urls.defaults import patterns
from two.ol.base import twpatterns
from wheelcms_axe.main import MainHandler

urlpatterns = patterns('',
    twpatterns("(?P<instance>.*)",
      MainHandler, name="wheel_main")
)
