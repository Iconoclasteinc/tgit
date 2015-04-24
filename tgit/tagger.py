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
import random
import sys

from PyQt5.QtCore import QTranslator, QLocale, QSettings
from PyQt5.QtWidgets import QApplication

from tgit.preferences import Preferences
from tgit.audio import MediaPlayer
from tgit.isni.name_registry import NameRegistry
from tgit.album_portfolio import AlbumPortfolio
from tgit import ui


def _start_local_isni_backend():
    import atexit
    from test.util import isni_database

    class RandomIsniResponses(object):
        def __init__(self):
            self.actions = ["0000000080183206", "0000000121707484", "sparse", "invalid data"]

        def __next__(self):
            return self.actions[random.randint(0, len(self.actions) - 1)]

    isni_database.persons["0000000080183206"] = [{"names": [("Joel", "Miller", "1969-")], "titles": ["Honeycombs"]}]
    isni_database.organisations["0000000121707484"] = [{"names": [
        "The Beatles", "Beatles, The"], "titles": [
        "The fool on the hill from The Beatles' T.V. film Magical mystery tour"]}]
    isni_database.assignation_generator = RandomIsniResponses()
    server_thread = isni_database.start()

    def shutdown_isni_database():
        isni_database.stop(server_thread)

    atexit.register(shutdown_isni_database)


def tgit(use_local_isni_backend=False):
    if use_local_isni_backend:
        _start_local_isni_backend()
        name_registry = NameRegistry(host="localhost", assign_host="localhost", port=5000)
    else:
        name_registry = NameRegistry(host="isni-m.oclc.nl", assign_host="isni-m-acc.oclc.nl", secure=True,
                                     username="ICON", password="crmeoS4d")

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