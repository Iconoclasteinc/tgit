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
from tgit.player import PhononPlayer
from tgit.producer import ProductionPortfolio, RecordLabel
from tgit.audio_library import AudioFiles
from tgit.ui.main_window import MainWindow
from tgit.ui.dialogs import AudioFileChooserDialog, ImageFileChooserDialog

TGIT = 'tgit'
QT = 'qt'
UTF_8 = 'UTF-8'


class TGiT(QApplication):
    def __init__(self, player=None, audioFileChooser=None, imageFileChooser=None):
        QApplication.__init__(self, [])

        if player is None:
            player = PhononPlayer()
        if audioFileChooser is None:
            audioFileChooser = AudioFileChooserDialog()
        if imageFileChooser is None:
            imageFileChooser = ImageFileChooserDialog()

        self._translators = []
        self._productions = ProductionPortfolio()

        self._ui = MainWindow(self._productions, player, audioFileChooser, imageFileChooser)
        self._attachFileChooser(audioFileChooser)
        self._attachFileChooser(imageFileChooser)
        self._addProductionHouseFor(AudioFiles())

    def show(self):
        self._ui.show()
        self._ui.raise_()
        self._ui.activateWindow()

    def _attachFileChooser(self, chooser):
        chooser.setParent(self._ui)

    def _addProductionHouseFor(self, audioLibrary):
        self._ui.addProductionHouse(RecordLabel(self._productions, audioLibrary))

    def useMediaPlayer(self, player):
        self._ui.setMediaPlayer(player)

    def useNativeDialogs(self, native):
        self._ui.useNativeDialogs(native)

    def translateInto(self, language):
        QTextCodec.setCodecForTr(QTextCodec.codecForName(UTF_8))
        for resource in (QT, TGIT):
            self._installTranslations(resource, language),

    def _installTranslations(self, resource, locale):
        translator = QTranslator()
        if translator.load('%s_%s' % (resource, locale), ':/resources'):
            self.installTranslator(translator)
            self._translators.append(translator)

    def run(self):
        self.show()
        return sys.exit(self.exec_())


def main(language):
    app = TGiT()
    app.translateInto(language)
    app.run()