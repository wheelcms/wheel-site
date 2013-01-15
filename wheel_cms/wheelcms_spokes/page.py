from django.db import models
from wheelcms_axle.models import type_registry
from wheelcms_spokes.templates import template_registry
from wheelcms_axle.models import Content
from wheelcms_spokes.models import Spoke

class Page(Content):
    """ A simple page object """
    body = models.TextField(blank=False)


class PageType(Spoke):
    model = Page

    title = "A simple HTML page"


type_registry.register(PageType)
template_registry.register(PageType, "wheelcms_spokes/page_view.html", "Basic Page view", default=True)
template_registry.register(PageType, "wheelcms_spokes/page_view_frontpage.html", "Frontpage Page view")
