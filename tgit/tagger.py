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

from tgit.audio import MediaPlayer, create_media_library
from tgit.isni.name_registry import NameRegistry
from tgit.preferences import Preferences
from tgit.album_portfolio import AlbumPortfolio
from tgit import ui


class TGiT(QApplication):
    def __init__(self, create_player, name_registry, native=True, confirm_exit=True, on_exit=None):
        super().__init__([])
        self._on_exit = on_exit
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

    def launch(self, preferences):
        self.show(preferences)
        self.run()

    def run(self):
        exit_value = self.exec_()
        self._player.close()
        self._media_library.close()
        if self._on_exit is not None:
            self._on_exit()
        sys.exit(exit_value)


def main():
    from requests.packages import urllib3
    urllib3.disable_warnings()

    from test.util.platform import isni_api
    server_thread = isni_api.start("isni.oclc.nl", 80)

    def shutdown_isni_api():
        isni_api.stop(server_thread)

    name_registry = NameRegistry(host="localhost", port=5001, secure=False)
    tagger = TGiT(MediaPlayer, name_registry, on_exit=shutdown_isni_api)
    tagger.launch(Preferences(QSettings()))
