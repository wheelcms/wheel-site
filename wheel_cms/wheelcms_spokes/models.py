from django.db import models
from django import forms
from wheelcms_axe.models import Content
from wheelcms_axe.models import type_registry


def formfactory(type):
    class Form(forms.ModelForm):
        class Meta:
            model = type
            exclude = ["node", "meta_type"]
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
## type_registry.register(PageType)

type_registry.register("page", Page, formfactory(Page))
type_registry.register("news", News, formfactory(News))
