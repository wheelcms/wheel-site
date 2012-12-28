from django.contrib import admin
from wheelcms_axe import models

class NodeAdmin(admin.ModelAdmin):
    model = models.Node


admin.site.register(models.Node, NodeAdmin)
