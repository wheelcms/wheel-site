from wheel_spokes.models import Page as PageModel
import wheel_axe.registry

class Page(object):
    name = "Page"

    model = PageModel

wheel_axe.registry.register_spoke(Page)
