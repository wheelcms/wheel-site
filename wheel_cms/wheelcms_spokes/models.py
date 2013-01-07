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

        # import pdb; pdb.set_trace()
        templates = template_registry.get(self._meta.model, [])
        self.fields['template'] = forms.ChoiceField(choices=templates, required=False)

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

    def clean_template(self):
        template = self.data.get('template')
        if not template:
            return ""

        if not template_registry.valid_for_model(self._meta.model, template):
            raise forms.ValidationError("Invalid template")
        return template


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
        if not self.o.template or \
           not template_registry.valid_for_model(self.model, self.o.template):
            default = template_registry.defaults.get(self.model)
            if not default:
                return "wheelcms_axle/content_view.html"
            return default

        return self.o.template

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


class News(Content):
    """ A news object """
    intro = models.TextField(blank=False)
    body = models.TextField(blank=False)

class NewsType(Spoke):
    model = News

    title = "A simple News item"


type_registry.register(PageType)
type_registry.register(NewsType)

class TemplateRegistry(dict):
    def __init__(self, *arg, **kw):
        super(TemplateRegistry, self).__init__(*arg, **kw)
        self.defaults = {}

    def valid_for_model(self, model, template):
        return template in dict(self.get(model, []))

    def register(self, spoke, template, title, default=False):
        if spoke.model not in self:
            self[spoke.model] = []

        self[spoke.model].append((template, title))

        if default:
            self.defaults[spoke.model] = template

template_registry = TemplateRegistry()

template_registry.register(PageType, "wheelcms_spokes/page_view.html", "Basic Page view", default=True)
template_registry.register(PageType, "wheelcms_spokes/page_view_frontpage.html", "Frontpage Page view")
template_registry.register(NewsType, "wheelcms_spokes/news_view.html", "Basic News view", default=True)
