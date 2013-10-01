# -*- coding: utf-8 -*-

import os
import shutil
import tempfile
import mimetypes


def readContent(filename):
    return open(filename, "rb").read()


def guessMimeType(filename):
    return mimetypes.guess_type(filename)[0]


def makeCopy(originalFile):
    workingFile, path = tempfile.mkstemp(suffix='.mp3')
    try:
        shutil.copy(originalFile, path)
    finally:
        os.close(workingFile)
    return path


