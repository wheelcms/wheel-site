from django.contrib import admin
from wheelcms_spokes import models

class PageAdmin(admin.ModelAdmin):
    model = models.Page


admin.site.register(models.Page, PageAdmin)
