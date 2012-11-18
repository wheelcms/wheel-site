from two.ol.base import RESTLikeHandler
from wheelcms_axe.models import Node

class WheelRESTHandler(RESTLikeHandler):
    pass

class MainHandler(WheelRESTHandler):
    model = Node

    @classmethod
    def coerce(cls, i):
        """ map path to node """
        return i['instance']

    def view(self):
        """ frontpage / view """

        self.context['instance'] = self.instance
        return self.template("wheelcms_axe/main.html")
