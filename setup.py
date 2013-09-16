# -*- coding: utf-8 -*-

import sys
from cx_Freeze import setup, Executable

DATA_FILES = []

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

includes = ["sip", "atexit", "PyQt4.QtCore", "PyQt4.QtGui"]

setup(
    name='tgit',
    description='TGit',
    author='Iconoclaste',
    url='http://tagtamusique.com',
    download_url='https://bitbucket.org/tagtamusique/tgit',
    author_email='jr@iconoclaste.ca',
    version='0.2-snapshot',
    test_suite='tests',
    packages=['tgit'],
    scripts=[],
    data_files=DATA_FILES,
    options={"build_exe": {"includes": includes, "include_files": ["locales"]},
             "bdist_mac": {"iconfile": 'tgit.icns'},
             "bdist_dmg": {"volume_label": "TGiT"}},
    executables=[Executable(script="tgit.py", icon="tgit.icns", base=base)]
)
