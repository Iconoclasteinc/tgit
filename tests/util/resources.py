# -*- coding: utf-8 -*-

import os

__all__ = ['path']

PROJECT_DIR = os.path.join(os.path.dirname(__file__), '../..')
TEST_DIR = os.path.abspath(os.path.join(PROJECT_DIR, 'tests'))
TEST_RESOURCES_DIR = os.path.join(TEST_DIR, 'resources')


def path(name):
    return os.path.abspath(os.path.join(TEST_RESOURCES_DIR, name))
