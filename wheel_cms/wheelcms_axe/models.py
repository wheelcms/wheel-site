from django.db import models

WHEEL_NODE_BASECLASS = models.Model
WHEEL_CONTENT_BASECLASS = models.Model

class Node(WHEEL_NODE_BASECLASS):
    path = models.TextField(blank=False)

    ## parent
    ## position within parent

class Content(WHEEL_CONTENT_BASECLASS):
    node = models.OneToOneField(Node, related_name="content")
    title = models.TextField(blank=False)
    created = models.DateTimeField(null=True)
    modified = models.DateTimeField(null=True)
    publication = models.DateTimeField(null=True)
    expire = models.DateTimeField(null=True)

