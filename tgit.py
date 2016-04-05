#!/usr/bin/env python
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
from traceback import format_exception
import sys
import argparse

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from requests.packages import urllib3

from tgit.tagger import make_tagger


def _print_unhandled_exceptions():
    def exception_hook(exctype, value, traceback):
        for line in format_exception(exctype, value, traceback):
            print(line, file=sys.stderr)

    sys.excepthook = exception_hook


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", action="store_true", help="starts in debug mode")
args = parser.parse_args()
if args.debug:
    _print_unhandled_exceptions()
    urllib3.disable_warnings()

app = QApplication([])
app.setApplicationName("TGiT")
app.setOrganizationName("Iconoclaste Inc.")
app.setOrganizationDomain("tagyourmusic.com")
app.setWindowIcon(QIcon(":/tgit.ico"))

make_tagger(app).show()
app.exec_()
