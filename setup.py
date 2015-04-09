# -*- coding: utf-8 -*-
import os
import sys
import PyQt5

from PyQt5.QtCore import QCoreApplication
from cx_Freeze import setup, Executable

from tgit import __version__


# Detect system
windows = sys.platform == 'win32'
osx = sys.platform == 'darwin'

# Assume there is a single plugins installation directory named plugins
plugins_path = next(path for path in QCoreApplication.libraryPaths() if path.endswith('plugins'))

# We need the media plugins
library_files = [(os.path.join(plugins_path, 'mediaservice'), 'mediaservice')]

# cx_Freeze is missing libEGL.dll, so include it ourselves
if windows:
    library_files.append((os.path.join(os.path.dirname(PyQt5.__file__), 'libEGL.dll'), 'libEGL.dll'))

options = {
    'includes': ['lxml._elementpath', 'lxml', 'PyQt5.QtNetwork', 'PyQt5.QtPrintSupport', 'PyQt5.QtMultimediaWidgets',
                 'PyQt5.QtOpenGL', 'PyQt5.QtSvg'],
    'include_files': library_files
}

setup(
    name='tgit',
    description='TGiT',
    author='Iconoclaste',
    url='http://tagyourmusic.com',
    download_url='https://bitbucket.org/iconoclaste/tgit',
    author_email='jr@iconoclaste.ca',
    version=__version__,
    test_suite='test',
    packages=['tgit'],
    scripts=['tgit.py'],
    options={'build_exe': options},
    executables=[Executable('tgit.py',
                            base='Win32GUI' if windows else None,
                            icon='tgit.ico' if windows else None,
                            appendScriptToExe=True if windows else False,
                            appendScriptToLibrary=False,)]
)