from two.ol.base import RESTLikeHandler
from wheelcms_axe.models import Node, Page
from django import forms

class WheelRESTHandler(RESTLikeHandler):
    pass

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        exclude = ["node", "meta_type"]

class MainHandler(WheelRESTHandler):
    model = Node
    formclass = PageForm

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
            self.context['form'] = PageForm()
        return self.template("wheelcms_axe/create.html")

    def view(self):
        """ frontpage / view """
        self.context['instance'] = self.instance
        return self.template("wheelcms_axe/main.html")

    def list(self):
        self.instance = Node.root()
        return self.view()
