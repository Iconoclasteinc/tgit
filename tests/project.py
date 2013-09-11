# -*- coding: utf-8 -*-

import os

test_dir = os.path.dirname(__file__)
test_resources_dir = os.path.join(test_dir, 'resources')
root_dir = os.path.normpath(os.path.join(test_dir, '..'))
locales_dir = os.path.join(root_dir, 'locales')


def test_resource(filename):
    return os.path.join(test_resources_dir, filename)
