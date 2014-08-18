# -*- coding: utf-8 -*-

import os

__all__ = ['path', 'normalizePath']

PROJECT_DIR = os.path.join(os.path.dirname(__file__), '../..')
TEST_DIR = os.path.abspath(os.path.join(PROJECT_DIR, 'test'))
TEST_RESOURCES_DIR = os.path.join(TEST_DIR, 'resources')


def root():
    return TEST_RESOURCES_DIR


def path(filepath, *more):
    filename = os.path.join(root(), filepath)
    for filepath in more:
        filename = os.path.join(filename, filepath)

    return normalizePath(os.path.abspath(filename))


def normalizePath(filepath):
    return filepath.replace("\\", "/")
