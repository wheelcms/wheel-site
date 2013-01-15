"""
    type specific test based on spoke base tests
"""
from wheelcms_spokes.tests.test_spoke import BaseSpokeTest, BaseSpokeTemplateTest
from wheelcms_spokes.page import PageType


class TestPageSpokeTemplate(BaseSpokeTemplateTest):
    """ Test the Page type """
    type = PageType
    typename = "page"

    def valid_data(self):
        """ return additional data for Page validation """
        return dict(body="Hello World")


class TestPageSpoke(BaseSpokeTest):
    """ Test the Page type """
    type = PageType
    typename = "page"
