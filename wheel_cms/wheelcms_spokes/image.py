from django.db import models
from wheelcms_axle.models import type_registry
from wheelcms_spokes.templates import template_registry
from wheelcms_axle.models import Content
from wheelcms_spokes.models import Spoke


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
