# -*- coding: utf-8 -*-

import os

testDir = os.path.dirname(__file__)
testResourcesDir = os.path.join(testDir, '../resources')
rootDir = os.path.abspath(os.path.join(testDir, '../../'))
localesDir = os.path.join(rootDir, '../../locales')


def testResourcePath(filename):
    return os.path.abspath(os.path.join(testResourcesDir, filename))
