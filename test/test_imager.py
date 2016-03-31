# -*- coding: utf-8 -*-
import os

from PyQt5.QtGui import QImage
from hamcrest import assert_that, equal_to, not_, empty

from test.util import resources
from testing.matchers import image_with
from tgit import imager, fs
from tgit.metadata import Image


def test_scaling_a_null_image_is_a_no_op():
    scaled_image = imager.scale(null_image(), 50, 50)

    assert_that(scaled_image.data, equal_to(b''), "empty scaled image")


def test_scales_image_to_specified_size_preserving_image_attributes():
    original_image = image_file(resources.path("front-cover.jpg"))
    scaled_image = imager.scale(original_image, 50, 50)

    assert_that(scaled_image, image_with(data=not_(empty()),
                                         mime=original_image.mime,
                                         type_=original_image.type,
                                         desc=original_image.desc), "scaled image")

    picture = QImage.fromData(scaled_image.data, imager.format_for(original_image.mime))
    assert_that(picture.width(), equal_to(50), "width")
    assert_that(picture.height(), equal_to(50), "height")


def null_image():
    return Image(mime="...", data=b'')


def image_file(path):
    return Image(mime=fs.guess_mime_type(path), data=fs.read(path), desc=os.path.basename(path))
