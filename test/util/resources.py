# -*- coding: utf-8 -*-

import os

__all__ = ['path']

PROJECT_DIR = os.path.join(os.path.dirname(__file__), '../..')
TEST_DIR = os.path.abspath(os.path.join(PROJECT_DIR, 'test'))
TEST_RESOURCES_DIR = os.path.join(TEST_DIR, 'resources')


def root():
    return TEST_RESOURCES_DIR


def path(path, *more):
    filename = os.path.join(root(), path)
    for path in more:
        filename = os.path.join(filename, path)

    return os.path.abspath(filename)
