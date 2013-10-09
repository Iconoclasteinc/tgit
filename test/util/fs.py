# -*- coding: utf-8 -*-

import os
import shutil
import tempfile
import mimetypes


def readContent(filename):
    return open(filename, "rb").read()


def guessMimeType(filename):
    return mimetypes.guess_type(filename)[0]


def makeCopy(filename):
    _, ext = os.path.splitext(filename)
    copy, path = tempfile.mkstemp(suffix=ext)
    shutil.copy(filename, path)
    os.close(copy)
    return path

