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
from PyQt4.QtCore import Qt, QTextCodec, QTranslator
from PyQt4.QtGui import QApplication

# noinspection PyUnresolvedReferences
from tgit import resources
from tgit.producer import ProductionPortfolio, RecordLabel
from tgit.audio_library import AudioFiles
from tgit.ui.main_window import MainWindow

TGIT = "tgit"
QT = "qt"
UTF_8 = "UTF-8"


class TGiT(QApplication):
    def __init__(self):
        QApplication.__init__(self, [])
        self._translators = []

        self._productions = ProductionPortfolio()
        self._ui = MainWindow(self._productions)
        self._addProductionHouseFor(AudioFiles())

    def _addProductionHouseFor(self, audioLibrary):
        self._ui.addProductionHouse(RecordLabel(self._productions, audioLibrary))

    def useMediaPlayer(self, player):
        self._ui.setMediaPlayer(player)

    def translateInto(self, language):
        QTextCodec.setCodecForTr(QTextCodec.codecForName(UTF_8))
        for resource in (QT, TGIT):
            self._installTranslations(resource, language),

    def _installTranslations(self, resource, locale):
        translator = QTranslator()
        if translator.load("%s_%s" % (resource, locale), ":/resources"):
            self.installTranslator(translator)
            self._translators.append(translator)

    def run(self):
        return sys.exit(self.exec_())


def main(language):
    app = TGiT()
    # todo use a native dialog by default in production mode
    app.translateInto(language)
    app.run()