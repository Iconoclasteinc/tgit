#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

import PyQt5
from cx_Freeze import setup, Executable
from tgit.version import __version__

windows = sys.platform == 'win32'
osx = sys.platform == 'darwin'

app_script = 'tgit.py'
app_package = 'tgit'
app_name = 'TGiT'
app_version = __version__
app_publisher = 'Iconoclaste Musique, Inc.'
app_publisher_email = 'jr@iconoclaste.ca'
app_url = 'http://www.tagyourmusic.com/'
app_download_url = 'https://bitbucket.org/iconoclaste/tgit/downloads'
app_exe = 'TGiT.exe' if windows else 'TGiT'
app_icon = 'resources/tgit.ico' if windows else 'resources/tgit.icns'
app_source_path = os.getcwd()
app_build_dir = os.path.join(app_source_path, r'build\exe.win-amd64-3.4') if windows else None
app_pyqt_path = os.path.dirname(PyQt5.__file__)
app_base = 'Win32GUI' if windows else None

include_files = [(os.path.join(app_pyqt_path, r'plugins/mediaservice'), 'mediaservice')]
includes = [
    'lxml._elementpath',
    'lxml', 'PyQt5.QtNetwork',
    'PyQt5.QtPrintSupport',
    'PyQt5.QtMultimediaWidgets',
    'PyQt5.QtOpenGL',
    'PyQt5.QtSvg'
]

if windows:
    include_files.append((os.path.join(app_pyqt_path, 'libEGL.dll'), 'libEGL.dll'))

    translation_file = os.path.join(app_source_path, 'resources/tgit_fr.ts')
    compiled_translation_file = os.path.join(app_source_path, 'resources/tgit_fr.qm')
    resources_file = os.path.join(app_source_path, 'resources/resources.qrc')
    compiled_resources_file = os.path.join(app_source_path, 'tgit/ui/resources.py')

    os.system('lrelease.exe %(translation_file)s -qm %(compiled_translation_file)s' % locals())
    os.system('pyrcc5.exe -o %(compiled_resources_file)s %(resources_file)s' % locals())

setup(
    name=app_name,
    description=app_name,
    author=app_publisher,
    url=app_url,
    download_url=app_download_url,
    author_email=app_publisher_email,
    version=app_version,
    packages=[app_package],
    scripts=[app_script],
    options={
        'build_exe': {
            'include_msvcr': True,
            'includes': includes,
            'include_files': include_files,
            'excludes': ['Tkinter']
        }
    },
    executables=[Executable(app_script,
                            base=app_base,
                            icon=app_icon,
                            targetName=app_exe,
                            appendScriptToExe=True,
                            appendScriptToLibrary=True)]
)

if windows:
    try:
        with open('tgit.template.iss', 'r') as src, open('tgit.iss', 'w') as dst:
            lines = src.readlines()
            data = []
            for l in lines:
                l = l.replace('@APP_NAME@', app_name)
                l = l.replace('@APP_VERSION@', app_version)
                l = l.replace('@APP_PUBLISHER@', app_publisher)
                l = l.replace('@APP_URL@', app_url)
                l = l.replace('@APP_EXE_NAME@', app_exe)
                l = l.replace('@APP_SOURCE_PATH@', app_source_path)
                l = l.replace('@APP_ICON@', app_icon)
                l = l.replace('@APP_BUILD_DIR@', app_build_dir)
                data.append(l)
            dst.writelines(data)
        os.environ['PATH'] += ';C:\Program Files (x86)\Inno Setup 5'
        os.system('iscc.exe %s' % os.path.join(app_source_path, 'tgit.iss'))
    except Exception as e:
        print(e)