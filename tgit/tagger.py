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
from traceback import format_exception

from PyQt5.QtCore import QTranslator, QLocale
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from tgit import ui
from tgit.album_portfolio import AlbumPortfolio
from tgit.audio import MediaPlayer, create_media_library
from tgit.cheddar import Cheddar
from tgit.settings_backend import SettingsBackend


class TGiT(QApplication):
    def __init__(self, create_player, cheddar, settings_file=None, native=True, confirm_exit=True, on_exit=None):
        super().__init__([])

        self.setApplicationName("TGiT")
        self.setOrganizationName("Iconoclaste Inc.")
        self.setOrganizationDomain("tagyourmusic.com")
        self.setWindowIcon(QIcon(":/tgit.ico"))

        self._settings_backend = SettingsBackend(settings_file)
        self._cheddar = cheddar
        self._on_exit = on_exit
        self._confirm_exit = confirm_exit
        self._native = native
        self._media_library = create_media_library()
        self._player = create_player(self._media_library)
        self._album_portfolio = AlbumPortfolio()
        self._album_portfolio.album_removed.subscribe(lambda album: self._player.stop())
        self._translators = []

    def _set_locale(self, locale):
        QLocale.setDefault(locale)
        for resource in ("qtbase", "tgit"):
            self._install_translations(resource, locale)

    def _install_translations(self, resource, locale):
        translator = QTranslator()
        if translator.load("{0}_{1}".format(resource, locale.name()), ":/"):
            self.installTranslator(translator)
            self._translators.append(translator)

    def show(self):
        preferences = self._settings_backend.load_user_preferences()
        self._set_locale(preferences.locale)
        session = self._settings_backend.load_session()
        main_window = ui.create_main_window(session, self._album_portfolio, self._player, preferences,
                                            self._cheddar, self._native, self._confirm_exit)
        main_window.show()

    def launch(self):
        self.show()
        self.run()

    def run(self):
        self.clean_exit(self.exec_())

    def clean_exit(self, exit_value):
        self._player.close()
        self._media_library.close()
        if self._on_exit is not None:
            self._on_exit()
        sys.exit(exit_value)


def main():
    from requests.packages import urllib3
    urllib3.disable_warnings()
    # _print_unhandled_exceptions()

    cheddar = Cheddar(host="tagyourmusic.herokuapp.com", port=443, secure=True)

    tagger = TGiT(MediaPlayer, cheddar)
    tagger.launch()


def _print_unhandled_exceptions():
    def exception_hook(exctype, value, traceback):
        for line in format_exception(exctype, value, traceback):
            print(line, file=sys.stderr)

    sys.excepthook = exception_hook
