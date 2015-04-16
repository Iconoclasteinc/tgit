#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from distutils.cmd import Command

import sys
import os

import PyQt5
from PyQt5.QtCore import QCoreApplication
from cx_Freeze import setup, Executable
from tgit import __version__

windows = sys.platform == 'win32'

app_script = 'tgit.py'
app_package = 'tgit'
app_name = 'TGiT'
app_version = __version__
app_publisher = 'Iconoclaste Musique, Inc.'
app_publisher_email = 'jr@iconoclaste.ca'
app_url = 'http://www.tagyourmusic.com/'
app_download_url = 'https://bitbucket.org/iconoclaste/tgit/downloads'
app_exe = 'TGiT.exe' if windows else 'tgit'
app_icon = 'resources/tgit.ico' if windows else 'resources/tgit.icns'
app_plist = 'resources/Info.plist'
app_source_path = os.getcwd()
app_build_dir = os.path.join(app_source_path, r'build\exe.win-amd64-3.4') if windows else None
app_base = 'Win32GUI' if windows else None

if windows:
    qt_path = os.path.dirname(PyQt5.__file__)
    qt_plugins_path = os.path.join(qt_path, 'plugins')
else:
    qt_plugins_path = next(path for path in QCoreApplication.libraryPaths() if path.endswith('plugins'))
    qt_path = os.path.dirname(qt_plugins_path)

include_files = [(os.path.join(qt_plugins_path, 'mediaservice'), 'mediaservice')]
if windows:
    include_files.append((os.path.join(qt_path, 'libEGL.dll'), 'libEGL.dll'))

includes = [
    'lxml._elementpath',
    'PyQt5.QtNetwork',
]


class translate(Command):
    description = "translate and compile qt resource files"
    # List of option tuples: long name, short name (None if no short name), and help string.
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        qt_binaries_path = qt_path if windows else os.path.join(qt_path, 'bin')
        translation_file = os.path.join(app_source_path, 'resources/tgit_fr.ts')
        compiled_translation_file = os.path.join(app_source_path, 'resources/tgit_fr.qm')
        os.system('%(qt_binaries_path)s/lrelease %(translation_file)s -qm %(compiled_translation_file)s' % locals())

        resources_file = os.path.join(app_source_path, 'resources/resources.qrc')
        compiled_resources_file = os.path.join(app_source_path, 'tgit/ui/resources.py')
        os.system('pyrcc5 -o %(compiled_resources_file)s %(resources_file)s' % locals())


class bdist_innosetup(Command):
    description = "create an InnoSetup installer (.exe) binary distribution"
    # List of option tuples: long name, short name (None if no short name), and help string.
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
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


class bdist_wix(Command):
    description = "create a MSI (.msi) binary distribution"
    # List of option tuples: long name, short name (None if no short name), and help string.
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        app_msi_dir = os.path.join(app_source_path, r'build\msi')
        if not os.path.exists(app_msi_dir):
            os.makedirs(app_msi_dir)

        with open('tgit.template.wxs', 'r') as src, open(os.path.join(app_msi_dir, r'tgit.wxs'), 'w') as dst:
            lines = src.readlines()
            data = []
            for l in lines:
                l = l.replace('@APP_NAME@', app_name)
                l = l.replace('@APP_VERSION@', app_version)
                l = l.replace('@APP_PUBLISHER@', app_publisher)
                l = l.replace('@APP_ICON@', app_icon)
                data.append(l)
            dst.writelines(data)
        os.environ['PATH'] += ';C:\\Program Files (x86)\\WiX Toolset v3.9\\bin'
        os.system('heat.exe dir %(app_build_dir)s -gg -sfrag -cg TgitComponent -nologo -dr INSTALLFOLDER -sreg -srd -out %(app_msi_dir)s\\tgit-dir.wxs' % {"app_build_dir": app_build_dir, "app_msi_dir": app_msi_dir})
        os.system('candle.exe %(app_msi_dir)s\\*.wxs -nologo -out %(app_msi_dir)s\\ ' % {"app_msi_dir": app_msi_dir})
        os.system('light.exe -b %(app_build_dir)s -nologo -ext WixUIExtension -cultures:en-us %(app_msi_dir)s\\*.wixobj -o build\\%(app_name)s-%(app_version)s.msi' % {"app_build_dir": app_build_dir, "app_msi_dir": app_msi_dir, "app_name": app_name, "app_version": app_version})


commands = {"translate": translate}
if windows:
    commands["bdist_inno"] = bdist_innosetup
    commands["bdist_wix"] = bdist_wix


setup(
    cmdclass=commands,
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
        },
        'bdist_mac': {
            'iconfile': app_icon,
            'qt_menu_nib': os.path.join(qt_path, 'qt_menu.nib'),
            'bundle_name': app_exe,
            'custom_info_plist': app_plist,
        },
        'bdist_dmg': {
            'volume_label': app_name,
            'applications_shortcut': True
        }
    },
    executables=[Executable(app_script,
                            base=app_base,
                            icon=app_icon,
                            targetName=app_exe,
                            appendScriptToExe=True,
                            appendScriptToLibrary=True)]
)


