# -*- coding: utf-8 -*-

from setuptools import setup

# noinspection PyUnresolvedReferences
import use_sip_api_v2

from tgit import __version__

setup(
    name='tgit',
    description='TGit',
    author='Iconoclaste',
    url='http://tagtamusique.com',
    download_url='https://bitbucket.org/tagtamusique/tgit',
    author_email='jr@iconoclaste.ca',
    version=__version__,
    test_suite='test',
    py_modules=['use_sip_api_v2'],
    packages=['tgit'],
    scripts=['tgit.py'],
    requires=['mutagen', 'PyQt4']
)