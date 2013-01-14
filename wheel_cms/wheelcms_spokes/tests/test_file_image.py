"""
    test file/image based on spoke base tests
"""

from wheelcms_spokes.tests.test_spoke import BaseCombinedSpokeTest
from wheelcms_spokes.models import ImageType, FileType
from django.core.files.uploadedfile import SimpleUploadedFile


class BaseImageFileTest(BaseCombinedSpokeTest):
    """
        Shared customization/tests
    """
    def valid_files(self):
        """ return an image, will work for both file and image uploads """
        return dict(storage=SimpleUploadedFile("foo.png", 
                    'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00'
                    '\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'))

    def test_children_restriction(self, client):
        """ by default, a file or image can't have kids """
        assert self.type.children is not None
        assert len(self.type.children) == 0


class TestImageSpoke(BaseImageFileTest):
    """
        Test the image spoke
    """
    type = ImageType
    typename = "image"


class TestFileSpoke(BaseImageFileTest):
    """
        Test the file spoke
    """
    type = FileType
    typename = "file"