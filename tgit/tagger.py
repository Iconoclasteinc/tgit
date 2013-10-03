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

from tgit.audio_player import PhononPlayer
from tgit.mp3 import MP3File
from tgit.ui.main_window import MainWindow

UTF_8 = "UTF-8"


class TGiT(QApplication):
    def __init__(self, locale, player):
        QApplication.__init__(self, [])
        self._translators = []
        self.setLocale(locale)
        self._ui = MainWindow(player)
        self._ui.addMusicDirector(MusicDirector(self._ui))

    def setLocale(self, locale):
        QTextCodec.setCodecForTr(QTextCodec.codecForName(UTF_8))
        self._installTranslator("qt", locale),
        self._installTranslator("tgit", locale)

    def _installTranslator(self, resource, locale):
        translator = QTranslator()
        if translator.load("%s_%s" % (resource, locale), ":/locales"):
            self.installTranslator(translator)
            self._translators.append(translator)

    def run(self):
        return sys.exit(self.exec_())


class MusicDirector(object):
    def __init__(self, ui):
        self._ui = ui

    def importTrack(self, filename):
        track = MP3File(filename)
        self._ui.trackImported(track)

    def saveAlbum(self, album):
        for track in album:
            track.save()


def main(locale):
    # todo Qt complains if we create the Phonon player before the QApplication
    TGiT(locale, PhononPlayer()).run()