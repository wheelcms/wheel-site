from django.db import models
from django import forms
from wheelcms_axe.models import Content, Node
from wheelcms_axe.models import type_registry

class BaseForm(forms.ModelForm):
    class Meta:
        exclude = ["node", "meta_type"]

    slug = forms.Field(required=True)

    def __init__(self, parent=None, *args, **kwargs):
        """
            Django will put the extra slug field at the bottom, below
            all model fields. I want it just after the title field
        """
        super(BaseForm, self).__init__(*args, **kwargs)
        slug = self.fields.pop('slug')
        titlepos = self.fields.keyOrder.index('title')
        self.fields.insert(titlepos+1, 'slug', slug)
        self.parent = parent

    def clean_slug(self):
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


class Page(Content):
    """ A simple page object """
    body = models.TextField(blank=False)

class News(Content):
    """ A news object """
    intro = models.TextField(blank=False)
    body = models.TextField(blank=False)

##
## Idee: combineer Model, Form en type-metadata in een aparte class,
## e.g.
## class PageType(..):
##   model = Page
##   form = formfactory(..)
##   name = "spokes.page"
##   title = "A simple webpage"
##
## view template, allowed subcontent(-restrictions)
## type_registry.register(PageType)

type_registry.register("page", Page, formfactory(Page))
type_registry.register("news", News, formfactory(News))
