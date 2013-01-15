from django.db import models
from django import forms

from wheelcms_axle.models import type_registry
from wheelcms_spokes.templates import template_registry
from wheelcms_axle.models import Content
from wheelcms_spokes.models import Spoke, formfactory

from tinymce.widgets import TinyMCE
from tinymce.models import HTMLField

##
## Either HTMLField or TinyMCE widget. But a demonstration on how to alter
## a Spoke's form is also nice to have.

class Page(Content):
    """ A simple page object """
    body = models.TextField(blank=False)
    # body = HTMLField(blank=False)


class PageForm(formfactory(Page)):
    body = forms.CharField(widget=TinyMCE(), required=False)


class PageType(Spoke):
    model = Page

    title = "A simple HTML page"

    form = PageForm


type_registry.register(PageType)
template_registry.register(PageType, "wheelcms_spokes/page_view.html",
                           "Basic Page view", default=True)
template_registry.register(PageType, "wheelcms_spokes/page_view_frontpage.html",
                           "Frontpage Page view")
