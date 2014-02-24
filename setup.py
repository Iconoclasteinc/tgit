# -*- coding: utf-8 -*-

from setuptools import setup

# noinspection PyUnresolvedReferences
import use_sip_api_v2

setup(
    name='tgit',
    description='TGit',
    author='Iconoclaste',
    url='http://tagtamusique.com',
    download_url='https://bitbucket.org/tagtamusique/tgit',
    author_email='jr@iconoclaste.ca',
    version='0.9',
    test_suite='test',
    py_modules=['use_sip_api_v2'],
    packages=['tgit'],
    scripts=['tgit.py'],
    requires=['mutagen', 'PyQt4']
)