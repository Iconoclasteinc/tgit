# -*- coding: utf-8 -*-


import sys

from cx_Freeze import setup, Executable

from tgit import __version__


base = None
include_files = None

if sys.platform == 'win32':
    base = 'Win32GUI'
    include_files = [
        (r'C:\Python34\Lib\site-packages\PyQt5\plugins\mediaservice', 'mediaservice'),
        (r'C:\Python34\Lib\site-packages\PyQt5\libEGL.dll', 'libEGL.dll')
    ]
else:
    include_files = [(r'/usr/local/Cellar/qt5/5.4.0/plugins/mediaservice', 'mediaservice')]

setup(
    name='tgit',
    description='TGiT',
    author='Iconoclaste',
    url='http://tagyourmusic.com',
    download_url='https://bitbucket.org/tagtamusique/tgit',
    author_email='jr@iconoclaste.ca',
    version=__version__,
    test_suite='test',
    packages=['tgit'],
    scripts=['tgit.py'],
    options={
        'build_exe': {
            'includes': ['lxml._elementpath', 'lxml', 'PyQt5.QtNetwork', 'PyQt5.QtPrintSupport', 'PyQt5.QtMultimediaWidgets', 'PyQt5.QtOpenGL', 'PyQt5.QtSvg'],
            'include_files': include_files,
            'excludes': ['Tkinter']
        }
    },
    executables=[Executable('tgit.py',
                            base=base,
                            icon='tgit.ico',
                            appendScriptToExe=True,
                            appendScriptToLibrary=False,)]
)