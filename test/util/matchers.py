# -*- coding: utf-8 -*-

from hamcrest import equal_to, contains, has_length
from test.util import fs


def samePictureAs(filename):
    return contains(equal_to(fs.guessMimeType(filename)),
                    has_length(len(fs.readContent(filename))))