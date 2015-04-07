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

from PyQt5.QtCore import QTranslator, QLocale
from PyQt5.QtWidgets import QApplication

from tgit.album_portfolio import AlbumPortfolio
from tgit.tagging.id3_container import ID3Container
from tgit import ui


class TGiT(QApplication):
    def __init__(self, player, name_registry, native=True):
        QApplication.__init__(self, [])
        self.player = player
        self.name_registry = name_registry
        self.translators = []
        self.native = native
        self.mainWindow = None

    def setLocale(self, locale):
        if locale is None:
            locale = QLocale.system().name()

        for resource in ('qt', 'tgit'):
            self.installTranslations(resource, locale)

    def installTranslations(self, resource, locale):
        translator = QTranslator()
        if translator.load('%s_%s' % (resource, locale), ':/resources'):
            self.installTranslator(translator)
            self.translators.append(translator)

    def show(self, preferences):
        self.setLocale(preferences['language'])
        self.mainWindow = ui.createMainWindow(AlbumPortfolio(), self.player(), preferences, ID3Container(), self.name_registry, self.native)
        ui.showCenteredOnScreen(self.mainWindow)

    def launch(self, preferences):
        self.show(preferences)
        self.run()

    def run(self):
        return sys.exit(self.exec_())
