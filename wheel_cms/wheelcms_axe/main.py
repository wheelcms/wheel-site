from two.ol.base import RESTLikeHandler
from wheelcms_axe.models import Node, type_registry

class WheelRESTHandler(RESTLikeHandler):
    pass


class MainHandler(WheelRESTHandler):
    model = Node

    def update_context(self, request):
        super(MainHandler, self).update_context(request)
        self.context['type_registry'] = type_registry

    def formclass(self, data=None, instance=None):
        type = self.request.REQUEST.get('type')
        if type is None and self.instance:
            type = self.instance.content().meta_type

        if type is None:
            return None

        typeinfo = type_registry.get(type)
        
        return typeinfo['form'](data=data, instance=instance)

    @classmethod
    def coerce(cls, i):
        """ map path to node """
        if i.get('instance'):
            return Node.get("/" + i['instance'])

    def create(self, *a, **b):
        parent = Node.get("/" + self.kw.get('nodepath'))

        if self.post:
            if self.form.is_valid():
                p = self.form.save()
                sub = parent.add("x")
                sub.set(p)
                return self.redirect(parent.path, success="Ok")
        else:
            self.context['form'] = self.formclass()
        return self.template("wheelcms_axe/create.html")

    def view(self):
        """ frontpage / view """
        self.context['instance'] = self.instance
        return self.template("wheelcms_axe/main.html")

    def list(self):
        self.instance = Node.root()
        return self.view()
