from django.db import models
from django import forms
from wheelcms_axle.models import Content, Node
from wheelcms_axle.models import type_registry
from wheelcms_axle.workflows.default import DefaultWorkflow

from wheelcms_spokes.templates import template_registry

from two.ol.util import classproperty

class BaseForm(forms.ModelForm):
    class Meta:
        exclude = ["node", "meta_type", "owner"]

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

        templates = template_registry.get(self._meta.model, [])
        if templates:
            self.fields['template'] = forms.ChoiceField(choices=templates,
                                                        required=False)
        else:
            self.fields.pop('template')  ## will default to content_view

        self.fields['state'] = forms.ChoiceField(choices=self.workflow_choices(),
                                                 initial=self.workflow_default(),
                                                 required=False)
        if self.instance and self.instance.node and self.instance.node.isroot():
            self.fields.pop("slug")

    def workflow_choices(self):
        """
            return valid choices. Is actually context dependend (not all states
            can be reached from a given state)
        """
        spoke = type_registry.get(self._meta.model.get_name())
        return spoke.workflowclass.states

    def workflow_default(self):
        """
            Return default state for active workflow
        """
        spoke = type_registry.get(self._meta.model.get_name())
        return spoke.workflowclass.default

    def clean_slug(self):
        if self.attach:
            return

        slug = self.data.get('slug', '').strip().lower()
        if not Node.validpathre.match(slug):
            raise forms.ValidationError("Only numbers, letters, _-")
        try:
            existing = Node.objects.filter(path=self.parent.path + "/" + slug
                                          ).get()
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
        class Meta(BaseForm.Meta):
            model = type
            exclude = BaseForm.Meta.exclude + ["created", "modified"]
    return Form


class Spoke(object):
    model = Content
    workflowclass = DefaultWorkflow

    ## None means no restrictions, () means no subcontent allowed
    children = None 

    def __init__(self, o):
        self.o = o
        self.instance = o  ## keep self.o for backward compat

    @classproperty
    def form(cls):
        return formfactory(cls.model)

    @classmethod
    def name(cls):
        """ This needs namespacing. But a model determines its name based
            on the classname and doesn't know about namespaces or packages """
        return cls.model.get_name()  ## app_label

    @classmethod
    def title(cls):
        """ a default title """
        return cls.model._meta.object_name + " content"

    def workflow(self):
        return self.workflowclass(self)

    def view_template(self):
        if not self.o.template or \
           not template_registry.valid_for_model(self.model, self.o.template):
            default = template_registry.defaults.get(self.model)
            if default:
                return default

            all = template_registry.get(self.model, [])
            if len(all) == 1:
                return all[0][0]

            return "wheelcms_axle/content_view.html"

        return self.o.template

    def fields(self):
        """ iterate over fields in model """
        for i in self.o._meta.fields:
            yield (i.name, getattr(self.o, i.name))


class Page(Content):
    """ A simple page object """
    body = models.TextField(blank=False)


class PageType(Spoke):
    model = Page

    title = "A simple HTML page"


type_registry.register(PageType)
template_registry.register(PageType, "wheelcms_spokes/page_view.html", "Basic Page view", default=True)
template_registry.register(PageType, "wheelcms_spokes/page_view_frontpage.html", "Frontpage Page view")


class News(Content):
    """ A news object """
    intro = models.TextField(blank=False)
    body = models.TextField(blank=False)


class NewsType(Spoke):
    model = News

    title = "A simple News item"


template_registry.register(NewsType, "wheelcms_spokes/news_view.html", "Basic News view", default=True)
type_registry.register(NewsType)


class Image(Content):
    """ Holds an image.  """
    ## cannot be named image - that's used for the content base relation
    storage = models.ImageField(upload_to="images", blank=False)

class ImageType(Spoke):
    model = Image

    title = "An image"
    children = ()

template_registry.register(ImageType, "wheelcms_spokes/image_view.html", "Basic Image view", default=True)
type_registry.register(ImageType)

class File(Content):
    """ Holds a file """
    ## cannot be named file - that's used for the content base relation
    storage = models.FileField(upload_to="files", blank=False)

class FileType(Spoke):
    model = File

    title = "A file"
    children = ()

template_registry.register(FileType, "wheelcms_spokes/file_view.html", "Basic News view", default=True)
type_registry.register(FileType)
