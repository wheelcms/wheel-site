from django.db import models
from wheelcms_axle.models import type_registry
from wheelcms_spokes.templates import template_registry
from wheelcms_axle.models import Content
from wheelcms_spokes.models import Spoke

class News(Content):
    """ A news object """
    intro = models.TextField(blank=False)
    body = models.TextField(blank=False)


class NewsType(Spoke):
    model = News

    title = "A simple News item"


template_registry.register(NewsType, "wheelcms_spokes/news_view.html", "Basic News view", default=True)
type_registry.register(NewsType)
