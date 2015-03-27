# -*- coding: utf-8 -*-


import sys

from cx_Freeze import setup, Executable

from tgit import __version__


base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'includes': ["lxml._elementpath", "lxml", "PyQt5.QtNetwork", "PyQt5.QtPrintSupport", "PyQt5.QtMultimediaWidgets", "PyQt5.QtOpenGL", "PyQt5.QtSvg"],
        "include_files": [(r"/usr/local/Cellar/qt5/5.4.0/plugins/mediaservice", "mediaservice")]
    }
}

executables = [
    Executable('tgit.py', base=base)
]

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
    options=options,
    executables=executables
)