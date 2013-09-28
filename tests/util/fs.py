# -*- coding: utf-8 -*-

import mimetypes


def readContent(filename):
    return open(filename, "rb").read()


def guessMimeType(filename):
    return mimetypes.guess_type(filename)[0]
