from django.conf.urls.defaults import patterns
from two.ol.base import twpatterns
from wheelcms_axe.main import MainHandler

urlpatterns = patterns('',
    ## special case for /create and /edit (on root) -> /_/create and /_/edit
    twpatterns("_/(?P<nodepath>(.*))", MainHandler, name="wheel_main"),
    # twpatterns("(?P<instance>(_))", MainHandler, name="wheel_main"),
    twpatterns("(?P<instance>.*)", MainHandler, name="wheel_main"),
    twpatterns("/", MainHandler, name="wheel_main"),
)
