# -*- coding: utf-8 -*-
#
# TGiT, Music Tagger for Professionals
# Copyright (C) 2013 Iconoclaste Musique Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
import sys

from PyQt5.QtCore import QTranslator, QLocale, QSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
import requests

from tgit.audio import MediaPlayer, create_media_library
from tgit.isni.name_registry import NameRegistry
from tgit.preferences import Preferences
from tgit.album_portfolio import AlbumPortfolio
from tgit import ui


class TGiT(QApplication):
    def __init__(self, create_player, name_registry, native=True, confirm_exit=True):
        super().__init__([])
        self._confirm_exit = confirm_exit
        self._native = native
        self._name_registry = name_registry
        self._media_library = create_media_library()
        self._player = create_player(self._media_library)
        self._album_portfolio = AlbumPortfolio()
        self._album_portfolio.album_removed.subscribe(lambda album: self._player.stop())
        self._translators = []

        self.setApplicationName("TGiT")
        self.setOrganizationName("Iconoclaste Inc.")
        self.setOrganizationDomain("tagyourmusic.com")
        self.setWindowIcon(QIcon(":/tgit.ico"))

    def _set_locale(self, locale):
        if locale is None:
            locale = QLocale.system().name()

        for resource in ("qtbase", "tgit"):
            self._install_translations(resource, locale)

    def _install_translations(self, resource, locale):
        translator = QTranslator()
        if translator.load("{0}_{1}".format(resource, locale), ":/"):
            self.installTranslator(translator)
            self._translators.append(translator)

    def show(self, preferences):
        self._set_locale(preferences["language"])
        main_window = ui.create_main_window(self._album_portfolio, self._player, preferences, self._name_registry,
                                            self._native, self._confirm_exit)
        main_window.show()

    def launch(self, preferences=Preferences(QSettings())):
        self.show(preferences)
        self.run()

    def run(self):
        exit_value = self.exec_()
        self._player.close()
        self._media_library.close()
        sys.exit(exit_value)


def main():
    requests.packages.urllib3.disable_warnings()

    name_registry = NameRegistry(host="isni-m.oclc.nl",
                                 assign_host="isni-m-acc.oclc.nl",
                                 secure=True,
                                 username="ICON",
                                 password="crmeoS4d")

    tagger = TGiT(MediaPlayer, name_registry)
    tagger.launch()
