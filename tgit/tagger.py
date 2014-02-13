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

from PyQt4.QtCore import QTextCodec, QTranslator
from PyQt4.QtGui import QApplication
from tgit.album_portfolio import AlbumPortfolio

from tgit.audio.audio_library import AudioFiles
from tgit.audio.player import PhononPlayer
from tgit.ui.main_window import MainWindow
from tgit.ui import display

# noinspection PyUnresolvedReferences
from tgit.ui import resources


TGIT = 'tgit'
QT = 'qt'
UTF_8 = 'UTF-8'
RESOURCES = ':/resources'


class TGiT(QApplication):
    def __init__(self, player, codec=UTF_8):
        QApplication.__init__(self, [])
        self._player = player
        QTextCodec.setCodecForTr(QTextCodec.codecForName(codec))

    def _locale(self, locale):
        self._translators = []
        for resource in (QT, TGIT):
            self._installTranslations(resource, locale)

    locale = property(fset=_locale)

    def _installTranslations(self, resource, locale):
        translator = QTranslator()
        if translator.load('%s_%s' % (resource, locale), RESOURCES):
            self.installTranslator(translator)
            self._translators.append(translator)

    def show(self):
        self._ui = MainWindow(AlbumPortfolio(), self._player(AudioFiles()))
        display.centeredOnScreen(self._ui)

    def launch(self):
        self.show()
        self.run()

    def run(self):
        return sys.exit(self.exec_())


def main(locale):
    app = TGiT(PhononPlayer)
    app.locale = locale
    app.launch()