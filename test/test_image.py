# -*- coding: utf-8 -*-
from PyQt5.QtGui import QImage
from hamcrest import assert_that, equal_to, not_, empty

from test.util import resources
from tgit import image, fs


def test_skips_scaling_if_image_is_null():
    scaled_image = image.scale(b'', 50, 50)

    assert_that(scaled_image, equal_to(b''), "empty scaled image")


def test_scales_image_to_png_of_specified_size():
    scaled_image = image.scale(_load_test_image("front-cover.jpg"), 50, 50)

    assert_that(scaled_image, not_(empty()), "scaled image")
    picture = QImage.fromData(scaled_image, "PNG")
    assert_that(picture.width(), equal_to(50), "width")
    assert_that(picture.height(), equal_to(50), "height")


def _load_test_image(name):
    return fs.read(resources.path(name))
