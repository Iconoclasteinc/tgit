# -*- coding: utf-8 -*-

import os


__all__ = ['path', 'locales']


PROJECT_DIR = os.path.join(os.path.dirname(__file__), '../..')
LOCALES_DIR = os.path.join(PROJECT_DIR, 'locales')
TEST_DIR = os.path.abspath(os.path.join(PROJECT_DIR, 'tests'))
TEST_RESOURCES_DIR = os.path.join(TEST_DIR, 'resources')


def locales():
    return LOCALES_DIR


def path(name):
    return os.path.abspath(os.path.join(TEST_RESOURCES_DIR, name))
