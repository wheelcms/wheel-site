from wheelcms_spokes.models import Page as PageModel
import wheelcms_axe.registry

class Page(object):
    name = "Page"

    model = PageModel

wheelcms_axe.registry.register_spoke(Page)
