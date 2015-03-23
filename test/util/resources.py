# -*- coding: utf-8 -*-

import os
import sys
import tempfile

__all__ = ['path', 'makeTempDir']

PROJECT_DIR = os.path.join(os.path.dirname(__file__), '../..')
TEST_DIR = os.path.abspath(os.path.join(PROJECT_DIR, 'test'))
TEST_RESOURCES_DIR = os.path.join(TEST_DIR, 'resources')
MAXIMUM_WINDOWS_DIR_PATH_LENGTH = 260


def root():
    return TEST_RESOURCES_DIR


def path(filepath, *more):
    filename = os.path.join(root(), filepath)
    for filepath in more:
        filename = os.path.join(filename, filepath)

    return os.path.abspath(filename)


def makeTempDir():
    dirpath = tempfile.mkdtemp()

    if sys.platform.startswith("win"):
        from ctypes import create_unicode_buffer, windll

        longname = create_unicode_buffer(MAXIMUM_WINDOWS_DIR_PATH_LENGTH)
        windll.kernel32.GetLongPathNameW(unicode(dirpath), longname, MAXIMUM_WINDOWS_DIR_PATH_LENGTH)
        dirpath = longname.value

    return dirpath