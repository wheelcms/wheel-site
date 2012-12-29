from two.ol.base import RESTLikeHandler
from wheelcms_axe.models import Node, type_registry

class WheelRESTHandler(RESTLikeHandler):
    pass


class MainHandler(WheelRESTHandler):
    model = dict(instance=Node, parent=Node)
    instance = None
    parent = None

    def update_context(self, request):
        super(MainHandler, self).update_context(request)
        self.context['type_registry'] = type_registry

    def formclass(self, data=None, instance=None):
        if not self.instance:
            return None

        type = self.instance.content().meta_type

        if not type:
            return None

        typeinfo = type_registry.get(type)
        parent = self.instance.parent()
        return typeinfo['form'](parent=parent, data=data, instance=instance)

    @classmethod
    def coerce(cls, i):
        """
            coerce either a parent and instance, a parent or an instance.
            If there's both a parent and an instance, the instance is relative
            to the parent, so resolving needs to be done by combing them

            We're supporting the parent/instance combo (somewhat) but don't
            really need it - <instance>/update works fine, and no instance is
            required for /create
        """
        d = dict()
        # import pdb; pdb.set_trace()

        parent_path = ""
        if i.get('parent') is not None:
            parent_path = i['parent']
            if parent_path:
                parent_path = '/' + parent_path
            d['parent'] = Node.get(parent_path)

        if i.get('instance') is not None:
            d['instance'] = Node.get(parent_path + '/' + i['instance'])
        return d

    def create(self, *a, **b):
        type = self.request.REQUEST.get('type')
        formclass = type_registry.get(type)['form']

        parent = self.parent

        if self.post:
            self.form = formclass(data=self.request.POST, parent=parent)
            if self.form.is_valid():
                ## form validation should handle slug uniqueness (?)
                p = self.form.save()
                slug = self.form.cleaned_data['slug']
                sub = parent.add(slug)
                sub.set(p)
                return self.redirect(parent.path or '/', success="Ok")
        else:
            self.context['form'] = formclass()
        self.context['type'] = self.request.REQUEST['type']
        return self.template("wheelcms_axe/create.html")

    def update(self):
        instance = self.instance
        parent = instance.parent()

        type = instance.content().meta_type
        typeinfo = type_registry.get(type)
        formclass =  typeinfo['form']
        slug = instance.slug()

        if self.post:
            self.context['form'] = form = formclass(parent=parent,
                                                    data=self.request.POST,
                                                    instance=instance.content())

            if form.is_valid():
                form.save()
                ## handle changed slug
                slug = form.cleaned_data['slug']
                if slug != self.instance.slug():
                    self.instance.set_slug(slug)

                return self.redirect(instance.path, success="Updated")
        else:
            self.context['form'] = formclass(parent=parent, initial=dict(slug=slug), instance=instance.content())
        
        return self.template("wheelcms_axe/update.html")

    def view(self):
        """ frontpage / view """
        self.context['instance'] = self.instance
        return self.template("wheelcms_axe/main.html")

    def list(self):
        self.instance = Node.root()
        return self.view()
