from django.contrib import admin
from wheelcms_spokes import models
from wheelcms_axle.models import type_registry

## create an admin for all registered types

for spoke in type_registry.values():
    class SpokeAdmin(admin.ModelAdmin):
        model = spoke.model
    admin.site.register(spoke.model, SpokeAdmin)
