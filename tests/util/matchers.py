# -*- coding: utf-8 -*-

from tests.util import fs

from hamcrest.core import equal_to
from hamcrest.library import contains, has_length


def samePictureAs(filename):
    return contains(equal_to(fs.guessMimeType(filename)),
                    has_length(len(fs.readContent(filename))))