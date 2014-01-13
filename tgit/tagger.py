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

from tgit.audio.audio_library import AudioFiles
from tgit.audio.player import PhononPlayer
from tgit.record_label import AlbumPortfolio, RecordLabel
from tgit.mp3.track_files import TrackFiles
from tgit.mp3.id3_tagger import Id3Tagger
from tgit.ui.main_window import MainWindow
from tgit.ui.dialogs import AudioFileChooserDialog, ImageFileChooserDialog
from tgit.ui import display
# noinspection PyUnresolvedReferences
from tgit.ui import resources

TGIT = 'tgit'
QT = 'qt'
UTF_8 = 'UTF-8'


class TGiT(QApplication):
    def __init__(self, language, player=PhononPlayer, audioFileChooser=None, imageFileChooser=None):
        QApplication.__init__(self, [])
        self._translators = []
        self._albums = AlbumPortfolio()

        if audioFileChooser is None:
            audioFileChooser = AudioFileChooserDialog()
        if imageFileChooser is None:
            imageFileChooser = ImageFileChooserDialog()

        self.changeLanguage(language)
        self._ui = MainWindow(self._albums, player(AudioFiles()), audioFileChooser,
                              imageFileChooser)
        self._attachFileChooser(audioFileChooser)
        self._attachFileChooser(imageFileChooser)
        self._addProductionHouseFor(TrackFiles(Id3Tagger()))

    def show(self):
        display.centeredOnScreen(self._ui)

    def _attachFileChooser(self, chooser):
        chooser.setParent(self._ui)

    def _addProductionHouseFor(self, trackCatalog):
        self._ui.addProductionHouse(RecordLabel(self._albums, trackCatalog))

    def useMediaPlayer(self, player):
        self._ui.setMediaPlayer(player)

    def useNativeDialogs(self, native):
        self._ui.useNativeDialogs(native)

    def changeLanguage(self, language):
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
    app = TGiT(language)
    app.run()