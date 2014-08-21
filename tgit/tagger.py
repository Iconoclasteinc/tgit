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

from PyQt4.QtCore import QTextCodec, QTranslator, QLocale, QSettings
from PyQt4.QtGui import QApplication

from tgit.album_portfolio import AlbumPortfolio
from tgit.audio.audio_library import AudioFiles
from tgit.audio.player import PhononPlayer
from tgit.sources.isni import NameRegistry
from tgit.tagging.id3_container import ID3Container
from tgit.preferences import Preferences
from tgit import ui
from tgit.ui.helpers import display


class TGiT(QApplication):
    def __init__(self, player, nameRegistry, native=True):
        QApplication.__init__(self, [])
        self.player = player
        self.nameRegistry = nameRegistry
        self.translators = []
        self.native = native

    def setLocale(self, locale):
        if locale is None:
            locale = QLocale.system().name()
        QTextCodec.setCodecForTr(QTextCodec.codecForName('UTF-8'))
        for resource in ('qt', 'tgit'):
            self.installTranslations(resource, locale)

    def installTranslations(self, resource, locale):
        translator = QTranslator()
        if translator.load('%s_%s' % (resource, locale), ':/resources'):
            self.installTranslator(translator)
            self.translators.append(translator)

    def show(self, preferences):
        self.setLocale(preferences['language'])
        self.mainWindow = \
            ui.createMainWindow(AlbumPortfolio(), self.player(AudioFiles()), preferences, ID3Container(), self.nameRegistry, self.native)
        display.centeredOnScreen(self.mainWindow)

    def launch(self, preferences):
        self.show(preferences)
        self.run()

    def run(self):
        return sys.exit(self.exec_())


def main():
    app = TGiT(PhononPlayer, NameRegistry('localhost'))
    #app = TGiT(PhononPlayer, NameRegistry('isni.oclc.nl'))
    app.setApplicationName('TGiT')
    app.launch(Preferences(QSettings('tagtamusique.com', 'TGiT')))