"""
    Test spoke related code / forms / behaviour
"""

from wheelcms_axle.models import Node
from wheelcms_spokes.models import TemplateRegistry
import wheelcms_spokes.models
from wheelcms_axle.tests.models import Type1
from wheelcms_axle.tests.models import Type1Type

DEFAULT = "wheelcms_axle/content_view.html"

class TestSpoke(object):
    """
        Basic spoke testing
    """
    def test_name(self, client):
        """
            Name generation
        """
        type1 = Type1()
        type1.save()
        type1type = Type1Type(type1)

        assert type1type.name() == "type1"

    def test_fields(self, client):
        """
            Test the fields() method that iterates over the
            model instances fields
        """
        type1 = Type1()
        type1.save()
        type1type = Type1Type(type1)
        fields = dict(type1type.fields())

        assert 'title' in fields
        assert 't1field' in fields


class TestSpokeTemplate(object):
    """
        Test template related validation/behaviour
    """
    def setup(self):
        """ create a clean local registry, make sure it's used globally """
        self.reg = TemplateRegistry()
        wheelcms_spokes.models.template_registry = self.reg

    def test_empty(self, client):
        """ An empty registry """
        form = Type1Type.form()
        assert 'template' not in form.fields
        type1 = Type1()
        type1.save()
        assert Type1Type(type1).view_template() == DEFAULT

    def test_default(self, client):
        """ If there's a default, it should be used """
        type1 = Type1()
        type1.save()
        self.reg.register(Type1Type, "foo/bar", "foo bar", default=False)
        self.reg.register(Type1Type, "foo/bar2", "foo bar", default=True)
        self.reg.register(Type1Type, "foo/bar3", "foo bar", default=False)
        assert Type1Type(type1).view_template() == "foo/bar2"

    def test_explicit(self, client):
        """ unless there's an explicit other selection """
        self.reg.register(Type1Type, "foo/bar", "foo bar", default=False)
        self.reg.register(Type1Type, "foo/bar2", "foo bar", default=True)
        self.reg.register(Type1Type, "foo/bar3", "foo bar", default=False)
        type1 = Type1(template="foo/bar3")
        type1.save()
        assert Type1Type(type1).view_template() == "foo/bar3"

    def test_form_validation_fail(self, client):
        """ Only registered templates are allowed """
        self.reg.register(Type1Type, "foo/bar", "foo bar", default=False)
        form = Type1Type.form(data={'template':"bar/foo"})
        assert not form.is_valid()
        assert 'template' in form.errors

    def test_form_validation_success(self, client):
        """ In the end it should succeed """
        self.reg.register(Type1Type, "foo/bar", "foo bar", default=False)
        self.reg.register(Type1Type, "foo/bar2", "foo bar", default=True)
        self.reg.register(Type1Type, "foo/bar3", "foo bar", default=False)
        p = Node.root()
        form = Type1Type.form(parent=p, data={'slug':'s',
                                              'title':'t',
                                              'template':"foo/bar3"})
        assert form.is_valid()
        assert form.data['template'] == "foo/bar3"
