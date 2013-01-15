from django.db import models
from wheelcms_axle.models import type_registry
from wheelcms_spokes.templates import template_registry
from wheelcms_axle.models import Content
from wheelcms_spokes.models import Spoke

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
