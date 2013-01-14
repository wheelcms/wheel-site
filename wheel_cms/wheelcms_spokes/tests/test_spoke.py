"""
    Test spoke related code / forms / behaviour
"""

from wheelcms_axle.models import Node, TypeRegistry, type_registry
from wheelcms_spokes.models import TemplateRegistry
import wheelcms_spokes.models
from wheelcms_axle.tests.models import Type1Type

DEFAULT = "wheelcms_axle/content_view.html"

class BaseSpokeTest(object):
    """
        Basic spoke testing
    """
    type = None
    typename = None

    def setup(self):
        """ override the global registry """
        self.registry = TypeRegistry()
        type_registry.set(self.registry)
        self.registry.register(self.type)

    def test_name(self, client):
        """
            Name generation
        """
        model = self.type.model()
        model.save()
        spoke = self.type(model)

        assert spoke.name() == self.typename

    def test_fields(self, client):
        """
            Test the fields() method that iterates over the
            model instances fields
        """
        model = self.type.model()
        model.save()
        spoke = self.type(model)
        fields = dict(spoke.fields())

        assert 'title' in fields

        return fields  ## for additional tests


class BaseSpokeTemplateTest(object):
    """
        Test template related validation/behaviour
    """
    def valid_data(self):
        """ return formdata required for validation to succeed """
        return {}

    def valid_files(self):
        """ return formdata files required for validation to succeed """
        return {}

    def setup(self):
        """ create clean local registries, make sure it's used globally """
        self.reg = TemplateRegistry()
        wheelcms_spokes.models.template_registry = self.reg

        self.registry = TypeRegistry()
        type_registry.set(self.registry)
        self.registry.register(self.type)

    def test_empty(self, client):
        """ An empty registry """
        form = self.type.form()
        assert 'template' not in form.fields
        model = self.type.model()
        model.save()
        assert self.type(model).view_template() == DEFAULT

    def test_single(self, client):
        """ An single template registered """
        self.reg.register(self.type, "foo/bar", "foo bar", default=False)
        form = self.type.form()
        assert 'template' in form.fields
        assert form.fields['template'].choices == [('foo/bar', 'foo bar')]
        model = self.type.model()
        model.save()
        assert self.type(model).view_template() == 'foo/bar'

    def test_default(self, client):
        """ If there's a default, it should be used """
        model = self.type.model()
        model.save()
        self.reg.register(self.type, "foo/bar", "foo bar", default=False)
        self.reg.register(self.type, "foo/bar2", "foo bar", default=True)
        self.reg.register(self.type, "foo/bar3", "foo bar", default=False)
        assert self.type(model).view_template() == "foo/bar2"

    def test_explicit(self, client):
        """ unless there's an explicit other selection """
        self.reg.register(self.type, "foo/bar", "foo bar", default=False)
        self.reg.register(self.type, "foo/bar2", "foo bar", default=True)
        self.reg.register(self.type, "foo/bar3", "foo bar", default=False)
        model = self.type.model(template="foo/bar3")
        model.save()
        assert self.type(model).view_template() == "foo/bar3"

    def test_form_validation_fail(self, client):
        """ Only registered templates are allowed """
        self.reg.register(self.type, "foo/bar", "foo bar", default=False)
        form = self.type.form(data={'template':"bar/foo"})
        assert not form.is_valid()
        assert 'template' in form.errors

    def test_form_validation_success(self, client):
        """ In the end it should succeed """
        self.reg.register(self.type, "foo/bar", "foo bar", default=False)
        self.reg.register(self.type, "foo/bar2", "foo bar", default=True)
        self.reg.register(self.type, "foo/bar3", "foo bar", default=False)
        p = Node.root()
        data = self.valid_data()
        data['slug'] = 's'
        data['title'] = 't'
        data['template'] = 'foo/bar3'

        form = self.type.form(parent=p, data=data, files=self.valid_files())

        assert form.is_valid()
        assert form.data['template'] == "foo/bar3"


class TestType1Spoke(BaseSpokeTest):
    """
        Run base tests on test type 'type1'
    """
    type = Type1Type
    typename = "type1"

    def test_fields(self, client):
        """ base tests + extra field """
        fields = super(TestType1Spoke, self).test_fields(client)
        assert 't1field' in fields


class TestType1SpokeTemplate(BaseSpokeTemplateTest):
    """
        Run base template tests on test type 'type1'
    """
    type = Type1Type
    typename = "type1"
