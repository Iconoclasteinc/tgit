# -*- coding: utf-8 -*-

from cx_Freeze import setup, Executable

DATA_FILES = []

includes = ["sip", "atexit", "PyQt4.QtCore", "PyQt4.QtGui"]

setup(
    name='tgit',
    description='TGit',
    author='Iconoclaste',
    url='http://tagtamusique.com',
    download_url='https://bitbucket.org/tagtamusique/tgit',
    author_email='jr@iconoclaste.ca',
    version='0.1',
    test_suite='tests',
    packages=['tgit'],
    scripts=[],
    data_files=DATA_FILES,
    options={"build_exe": {"includes": includes}},
    executables=[Executable(script="tagger.py", icon="tgit.icns")]
)
