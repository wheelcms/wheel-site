from django.db import models
from wheelcms_axe.models import Node

class Page(models.Model):
    node = models.ForeignKey(Node, related_name="spoke_pages")
    body = models.TextField()

