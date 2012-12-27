from django.contrib import admin
from wheelcms_axe import models

class NodeAdmin(admin.ModelAdmin):
    model = models.Node

class PageAdmin(admin.ModelAdmin):
    model = models.Page


admin.site.register(models.Node, NodeAdmin)
admin.site.register(models.Page, PageAdmin)
