# -*- coding: utf-8 -*-

from setuptools import setup

from tgit import __version__
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
    packages=['tgit'],
    scripts=['tgit.py'],
    requires=['mutagen', 'python-dateutil', 'six', 'PyQt4']
)