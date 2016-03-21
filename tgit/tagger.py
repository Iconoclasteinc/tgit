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
from traceback import format_exception

from PyQt5.QtCore import QTranslator, QLocale
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QApplication

from tgit.album_portfolio import AlbumPortfolio
from tgit.audio import MediaPlayer, create_media_library
from tgit.cheddar import Cheddar
from tgit.settings_backend import SettingsBackend
from tgit.signal import MultiSubscription
from tgit.ui import make_main_window


def main():
    _disable_urllib_warnings()
    # _print_unhandled_exceptions()
    sys.exit(launch_tagger())


def launch_tagger():
    app = QApplication([])
    app.setApplicationName("TGiT")
    app.setOrganizationName("Iconoclaste Inc.")
    app.setOrganizationDomain("tagyourmusic.com")
    app.setWindowIcon(QIcon(":/tgit.ico"))

    # QSettings must be initialized _after_ the organization name is set on the QApplication
    settings = SettingsBackend()
    preferences = settings.load_user_preferences()
    cheddar = Cheddar(host="tagyourmusic.com", port=443, secure=True)
    media_library = create_media_library()
    player = MediaPlayer(media_library)
    portfolio = AlbumPortfolio()

    subscriptions = MultiSubscription()
    subscriptions += portfolio.album_removed.subscribe(lambda _: player.stop())

    app.lastWindowClosed.connect(cheddar.stop)
    app.lastWindowClosed.connect(player.close)
    app.lastWindowClosed.connect(media_library.close)
    app.lastWindowClosed.connect(subscriptions.cancel)

    _set_locale(app, preferences.locale)
    make_main_window(settings.load_session(), portfolio, player, preferences, cheddar).show()

    return app.exec_()


def _set_locale(app, locale):
    QLocale.setDefault(QLocale(locale))
    for resource in ("qtbase", "tgit"):
        _install_translations(app, resource, locale)


def _install_translations(app, resource, locale):
    translator = QTranslator(app)
    if translator.load("{0}_{1}".format(resource, locale), ":/"):
        app.installTranslator(translator)


def _disable_urllib_warnings():
    from requests.packages import urllib3
    urllib3.disable_warnings()


def _print_unhandled_exceptions():
    def exception_hook(exctype, value, traceback):
        for line in format_exception(exctype, value, traceback):
            print(line, file=sys.stderr)

    sys.excepthook = exception_hook
