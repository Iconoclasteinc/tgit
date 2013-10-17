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

from tgit.producer import AlbumTagger
# noinspection PyUnresolvedReferences
from tgit import resources
from tgit.album import Album
from tgit.audio_library import AudioFiles
from tgit.player import MediaPlayer
from tgit.ui.main_window import MainWindow

TGIT = "tgit"
QT = "qt"
UTF_8 = "UTF-8"


class TGiT(QApplication):
    def __init__(self, locale, player=None):
        QApplication.__init__(self, [])
        self._translators = []
        self.translateTo(locale)
        self._album = Album()
        self._ui = MainWindow(self._album, player or MediaPlayer())
        self._addMusicProducerFor(self._ui)

    def _addMusicProducerFor(self, ui):
        ui.addMusicProducer(AlbumTagger(self._album, AudioFiles()))

    def translateTo(self, locale):
        QTextCodec.setCodecForTr(QTextCodec.codecForName(UTF_8))
        for resource in (QT, TGIT):
            self._installTranslations(resource, locale),

    def _installTranslations(self, resource, locale):
        translator = QTranslator()
        if translator.load("%s_%s" % (resource, locale), ":/resources"):
            self.installTranslator(translator)
            self._translators.append(translator)

    def run(self):
        return sys.exit(self.exec_())


def main(locale):
    TGiT(locale).run()