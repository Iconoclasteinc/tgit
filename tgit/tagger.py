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

from tgit.preferences import Preferences
from tgit.audio import MediaPlayer, create_media_library as media_library
from tgit.isni.name_registry import NameRegistry
from tgit.album_portfolio import AlbumPortfolio
from tgit import ui


def tgit(use_local_isni_backend=False):
    if use_local_isni_backend:
        name_registry = NameRegistry(host="localhost", assign_host="localhost", port=5000)
    else:
        name_registry = NameRegistry(host="isni-m.oclc.nl", assign_host="isni-m-acc.oclc.nl", secure=True,
                                     username="ICON", password="crmeoS4d")

    app = TGiT(MediaPlayer, media_library, name_registry, use_local_isni_backend)
    app.setApplicationName("TGiT")
    app.setOrganizationName("Iconoclaste Inc.")
    app.setOrganizationDomain("tagyourmusic.com")
    app.setWindowIcon(QIcon(":/tgit.ico"))
    app.launch(Preferences(QSettings()))


class TGiT(QApplication):
    def __init__(self, create_player, create_media_library, name_registry, use_local_isni_backend=False, native=True,
                 confirm_exit=True):
        super().__init__([])
        self._confirm_exit = confirm_exit
        self._use_local_isni_backend = use_local_isni_backend
        self._media_library = create_media_library()
        self._player = create_player(self._media_library)
        self._name_registry = name_registry
        self._translators = []
        self._native = native
        self._main_window = None

    def set_locale(self, locale):
        if locale is None:
            locale = QLocale.system().name()

        for resource in ("qt", "tgit"):
            self.install_translations(resource, locale)

    def install_translations(self, resource, locale):
        translator = QTranslator()
        if translator.load("{0}_{1}".format(resource, locale), ":/"):
            self.installTranslator(translator)
            self._translators.append(translator)

    def show(self, preferences):
        self.set_locale(preferences["language"])
        self._main_window = ui.create_main_window(AlbumPortfolio(), self._player, preferences, self._name_registry,
                                                  self._use_local_isni_backend, self._native, self._confirm_exit)
        self._main_window.show()

    def launch(self, preferences):
        self.show(preferences)
        self.run()

    def run(self):
        exit_value = self.exec_()
        self._player.close()
        self._media_library.close()
        sys.exit(exit_value)
