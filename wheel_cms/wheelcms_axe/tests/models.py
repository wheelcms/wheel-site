from wheelcms_axe.models import Content
from wheelcms_spokes.models import formfactory

class Type1(Content):
    pass

class Type2(Content):
    pass


from wheelcms_axe.models import type_registry

type_registry.register("type1", Type1, formfactory(Type1))
type_registry.register("type2", Type1, formfactory(Type2))
