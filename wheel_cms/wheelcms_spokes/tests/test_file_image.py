"""
    test file/image based on spoke base tests
"""

from wheelcms_spokes.tests.test_spoke import BaseSpokeTemplateTest, BaseSpokeTest
from wheelcms_spokes.file import FileType
from wheelcms_spokes.image import ImageType
from django.core.files.uploadedfile import SimpleUploadedFile


class BaseImageFileTest(BaseSpokeTemplateTest):
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


class TestImageSpokeTemplate(BaseImageFileTest):
    """
        Test the image spoke
    """
    type = ImageType
    typename = "image"


class TestImageSpoke(BaseSpokeTest):
    """
        Test the image spoke
    """
    type = ImageType
    typename = "image"


class TestFileSpokeTemplate(BaseImageFileTest):
    """
        Test the file spoke
    """
    type = FileType
    typename = "file"


class TestFileSpoke(BaseSpokeTest):
    """
        Test the file spoke
    """
    type = FileType
    typename = "file"
