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
from PyQt4.Qt import QApplication, QTextCodec, QTranslator

from tgit.ui.main_window import MainWindow

UTF_8 = "UTF-8"


class TGiT(QApplication):
    def __init__(self, localesDir, locale='en'):
        QApplication.__init__(self, [])
        self._localesDir = localesDir
        self.locale = locale
        self._ui = MainWindow()
        self._show(self._ui)

    def _show(self, main_window):
        main_window.show()
        main_window.raise_()
        main_window.activateWindow()

    def locale(self, locale):
        QTextCodec.setCodecForTr(QTextCodec.codecForName(UTF_8))
        self._qtTranslations = self.installTranslations("qt", locale)
        self._appTranslations = self.installTranslations("tgit", locale)

    def installTranslations(self, file, locale):
        translator = QTranslator()
        if translator.load("%s_%s" % (file, locale), self._localesDir):
            self.installTranslator(translator)
            return translator
        else:
            return None

    locale = property(fset=locale)

    def run(self):
        return sys.exit(self.exec_())


def main(locales_dir):
    TGiT(locales_dir, locale='fr').run()
