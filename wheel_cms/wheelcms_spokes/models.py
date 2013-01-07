from django.db import models
from django import forms
from wheelcms_axle.models import Content, Node
from wheelcms_axle.models import type_registry

from two.ol.util import classproperty

class BaseForm(forms.ModelForm):
    class Meta:
        exclude = ["node", "meta_type"]

    slug = forms.Field(required=True)

    def __init__(self, parent=None, attach=False, *args, **kwargs):
        """
            Django will put the extra slug field at the bottom, below
            all model fields. I want it just after the title field
        """
        super(BaseForm, self).__init__(*args, **kwargs)
        slug = self.fields.pop('slug')
        titlepos = self.fields.keyOrder.index('title')
        self.fields.insert(titlepos+1, 'slug', slug)
        self.parent = parent
        self.attach = attach
        if attach:
            self.fields.pop('slug')

    def clean_slug(self):
        if self.attach:
            return

        slug = self.data.get('slug', '').strip().lower()
        if not Node.validpathre.match(slug):
            raise forms.ValidationError("Only numbers, letters, _-")
        try:
            existing = Node.objects.filter(path=self.parent.path + "/" + slug).get()
            if existing != self.instance.node:
                raise forms.ValidationError("Name in use")
        except Node.DoesNotExist:
            pass

        return slug

def formfactory(type):
    class Form(BaseForm):
        class Meta:
            model = type
            exclude = ["node", "meta_type", "created", "modified"]
    return Form


class Spoke(object):
    model = Content

    def __init__(self, o):
        self.o = o

    @classproperty
    def form(cls):
        return formfactory(cls.model)

    @classmethod
    def name(cls):
        """ This needs namespacing. But a model determines its name based
            on the classname and doesn't know about namespaces or packages """
        # import pytest; pytest.set_trace()
        # return cls.model.__class__.__name__.lower()
        return cls.model._meta.object_name.lower()  ## app_label

    @classmethod
    def title(cls):
        """ a default title """
        return cls.model._meta.object_name + " content"

    def view_template(self):
        return "wheelcms_axle/content_view.html"

    def fields(self):
        ## move to spokes
        for i in self.o._meta.fields:
            yield (i.name, getattr(self.o, i.name))
    ## allowed subchildren, if any, can be dynamic

class Page(Content):
    """ A simple page object """
    body = models.TextField(blank=False)

class PageType(Spoke):
    model = Page

    title = "A simple HTML page"

    def view_template(self):
        return "wheelcms_spokes/page_view.html"


class News(Content):
    """ A news object """
    intro = models.TextField(blank=False)
    body = models.TextField(blank=False)

class NewsType(Spoke):
    model = News

    title = "A simple News item"

    def view_template(self):
        return "wheelcms_spokes/news_view.html"

type_registry.register(PageType)
type_registry.register(NewsType)
