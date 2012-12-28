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
        if 'nodepath' in self.kw:
            parent = Node.get('/' + self.kw['nodepath'])
            ## if there's an instance, we're in update/edit mode in stead
            ## of create
        else:
            parent = None
        
        type = self.request.REQUEST.get('type')
        if type is None and self.instance:
            type = self.instance.content().meta_type

        if type is None:
            return None

        typeinfo = type_registry.get(type)
        
        return typeinfo['form'](parent=parent, data=data, instance=instance)

    @classmethod
    def coerce(cls, i):
        """ map path to node """
        if i.get('instance'):
            return Node.get("/" + i['instance'])

    def create(self, *a, **b):
        parent = Node.get("/" + self.kw.get('nodepath'))

        if self.post:
            if self.form.is_valid():
                ## form validation should handle slug uniqueness (?)
                p = self.form.save()
                slug = self.form.cleaned_data['slug']
                sub = parent.add(slug)
                sub.set(p)
                return self.redirect(parent.path, success="Ok")
        else:
            self.context['form'] = self.formclass()
        self.context['type'] = self.request.REQUEST['type']
        return self.template("wheelcms_axe/create.html")

    def view(self):
        """ frontpage / view """
        self.context['instance'] = self.instance
        return self.template("wheelcms_axe/main.html")

    def list(self):
        self.instance = Node.root()
        return self.view()
