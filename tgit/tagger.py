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
from PyQt5.QtWidgets import QApplication
from tgit.preferences import Preferences
from tgit.audio import MediaPlayer
from tgit.isni.name_registry import NameRegistry

from tgit.album_portfolio import AlbumPortfolio
from tgit import ui


def tgit():
    name_registry = NameRegistry(host="isni-m.oclc.nl", assign_host="isni-m-acc.oclc.nl", secure=True, username="ICON",
                                 password="crmeoS4d")

    app = TGiT(MediaPlayer, name_registry)
    app.setApplicationName("TGiT")
    app.setOrganizationName("Iconoclaste Inc.")
    app.setOrganizationDomain("tagyourmusic.com")
    app.launch(Preferences(QSettings()))


class TGiT(QApplication):
    def __init__(self, player, name_registry, native=True):
        super().__init__([])
        self.player = player
        self.name_registry = name_registry
        self.translators = []
        self.native = native
        self.mainWindow = None

    def set_locale(self, locale):
        if locale is None:
            locale = QLocale.system().name()

        for resource in ("qt", "tgit"):
            self.install_translations(resource, locale)

    def install_translations(self, resource, locale):
        translator = QTranslator()
        if translator.load("{0}_{1}".format(resource, locale), ":/"):
            self.installTranslator(translator)
            self.translators.append(translator)

    def show(self, preferences):
        self.set_locale(preferences["language"])
        self.mainWindow = ui.createMainWindow(AlbumPortfolio(), self.player(), preferences, self.name_registry,
                                              self.native)
        ui.showCenteredOnScreen(self.mainWindow)

    def launch(self, preferences):
        self.show(preferences)
        self.run()

    def run(self):
        return sys.exit(self.exec_())