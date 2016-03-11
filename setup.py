#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from distutils.cmd import Command

import PyQt5
import cx_Freeze
from PyQt5.QtCore import QCoreApplication
from cx_Freeze import setup, Executable

from tgit import __app_name__, __version__
from tgit.platforms import windows, mac

app_script = "tgit.py"
app_package = "tgit"
app_name = __app_name__
app_version = __version__
app_publisher = "Iconoclaste Musique, Inc."
app_publisher_email = "jr@iconoclaste.ca"
app_url = "http://www.tagyourmusic.com/"
app_download_url = "https://bitbucket.org/iconoclaste/tgit/downloads"
app_exe = "TGiT.exe" if windows else "TGiT"
app_icon = "resources/tgit.ico" if windows else "resources/tgit.icns"
app_plist = "resources/Info.plist"
app_source_path = os.getcwd()
app_build_dir = os.path.join(app_source_path, r"build\exe.win-amd64-3.4") if windows else None
app_base = "Win32GUI" if windows else None
wix_version = "3.10" if windows else ""

if windows:
    qt_path = os.path.dirname(PyQt5.__file__)
    qt_plugins_path = os.path.join(qt_path, "plugins")

if mac:
    qt_plugins_path = next(path for path in QCoreApplication.libraryPaths() if path.endswith("plugins"))
    qt_path = os.path.dirname(qt_plugins_path)

include_files = [(os.path.join(qt_plugins_path, "mediaservice"), "mediaservice")]
if windows:
    include_files.append((os.path.join(qt_path, "libEGL.dll"), "libEGL.dll"))

includes = [
    "PyQt5.QtNetwork",
    "tgit.ui.widgets.help_label",
    "tgit.ui.widgets.text_area",
    "tgit.ui.widgets.progress_indicator",
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
        qt_binaries_path = qt_path if windows else os.path.join(qt_path, "bin")
        app_translation_file = os.path.join(app_source_path, "resources/tgit_fr.ts")
        app_compiled_translation_file = os.path.join(app_source_path, "resources/tgit_fr.qm")
        os.system("{0}/lrelease {1} -qm {2}".format(qt_binaries_path, app_translation_file, app_compiled_translation_file))

        qt_translation_file = os.path.join(app_source_path, "resources/qtbase_fr.ts")
        qt_compiled_translation_file = os.path.join(app_source_path, "resources/qtbase_fr.qm")
        os.system("{0}/lrelease {1} -qm {2}".format(qt_binaries_path, qt_translation_file, qt_compiled_translation_file))

        resources_file = os.path.join(app_source_path, "resources/resources.qrc")
        compiled_resources_file = os.path.join(app_source_path, "tgit/ui/resources.py")
        os.system("pyrcc5 -o {0} {1}".format(compiled_resources_file, resources_file))


commands = {"translate": translate}

if windows:
    class bdist_wix(Command):
        description = "create a MSI (.msi) binary distribution"
        # List of option tuples: long name, short name (None if no short name), and help string.
        user_options = []

        def initialize_options(self):
            pass

        def finalize_options(self):
            pass

        def run(self):
            app_msi_dir = os.path.join(app_source_path, r"build\msi")
            if not os.path.exists(app_msi_dir):
                os.makedirs(app_msi_dir)

            with open("tgit.template.wxs", "r") as src, open(os.path.join(app_msi_dir, r"tgit.wxs"), "w") as dst:
                lines = src.readlines()
                data = []
                for l in lines:
                    l = l.replace("@APP_NAME@", app_name)
                    l = l.replace("@APP_VERSION@", app_version)
                    l = l.replace("@APP_PUBLISHER@", app_publisher)
                    l = l.replace("@APP_ICON@", app_icon)
                    data.append(l)
                dst.writelines(data)
            os.environ["PATH"] += ";C:\\Program Files (x86)\\WiX Toolset v{0}\\bin".format(wix_version)
            os.system("heat.exe dir {0} -gg -sfrag -cg TgitComponent -nologo -dr INSTALLFOLDER -sreg -srd -out {1}\\tgit-dir.wxs".format(app_build_dir, app_msi_dir))
            os.system("candle.exe {0}\\*.wxs -nologo -out {0}\\ ".format(app_msi_dir))
            os.system("light.exe -b {0} -nologo -ext WixUIExtension -cultures:en-us {1}\\*.wixobj -o build\\{2}-{3}.msi".format(app_build_dir, app_msi_dir, app_name, app_version))

    commands["bdist_wix"] = bdist_wix

if mac:
    class bdist_mac(cx_Freeze.bdist_mac):
        cx_Freeze.bdist_mac.user_options.append(('locales', None, 'List of supported locales'))

        def initialize_options(self):
            super().initialize_options()

            self.locales = ["en"]

        def run(self):
            super().run()

            for locale in self.locales:
                # .lproj folder needs to exist, but needn't have any content
                os.mkdir(os.path.join(self.resourcesDir, locale + ".lproj"))

    commands["bdist_mac"] = bdist_mac


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
        "build_exe": {
            "include_msvcr": True,
            "includes": includes,
            "include_files": include_files,
        },
        "bdist_mac": {
            "iconfile": app_icon,
            "qt_menu_nib": os.path.join(qt_path, "qt_menu.nib"),
            "bundle_name": app_exe,
            "custom_info_plist": app_plist,
            "locales": ["en", "fr"]
        },
        "bdist_dmg": {
            "volume_label": app_name,
            "applications_shortcut": True
        }
    },
    executables=[Executable(app_script,
                            base=app_base,
                            icon=app_icon,
                            targetName=app_exe,
                            appendScriptToExe=True,
                            appendScriptToLibrary=True)]
)
