from wheelcms_axe.models import Node
from wheelcms_axe.tests.models import Type1, Type2

from django.db import IntegrityError

import pytest

class TestContent(object):
    """ Test content / content-node related stuff """

    def test_duplicate_content(self, client):
        """ two content objects cannot point to the same node """
        root = Node.root()
        child1 = root.add("n1")
        Type1(node=child1).save()
        pytest.raises(IntegrityError, lambda: Type1(node=child1).save())

    def test_node_content(self, client):
        """ get the actual content instance through the node """
        root = Node.root()
        child1 = root.add("n1")
        c1 = Type1(node=child1)
        c1.save()
        child2 = root.add("n2")
        c2 = Type2(node=child2)
        c2.save()

        assert child1.content() == c1
        assert child2.content() == c2

    def test_node_set(self, client):
        """ test the node.set method """
        root = Node.root()
        child1 = root.add("n1")
        c1 = Type1()
        c1.save()
        child1.set(c1)
        c1 = Type1.objects.get(pk=c1.pk)  ## get updated state
        assert child1.content() == c1
        assert c1.node == child1

    def test_node_set_base(self, client):
        """ test the node.set method  with Content instance """
        root = Node.root()
        child1 = root.add("n1")
        c1 = Type1()
        c1.save()
        child1.set(c1.content_ptr)

        assert child1.content() == c1

    def test_node_set_replace(self, client):
        """ test the node.set method """
        root = Node.root()
        child1 = root.add("n1")
        c1 = Type1()
        c1.save()
        child1.set(c1)
        c2 = Type2()
        c2.save()
        old = child1.set(c2, replace=True)

        assert child1.content() == c2
        assert old == c1

