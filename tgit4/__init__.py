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
# noinspection PyUnresolvedReferences


def use_sip_api_v2():
    for name in ("QDate", "QDateTime", "QString", "QTextStream", "QTime", "QUrl", "QVariant"):
        sip.setapi(name, 2)


import sip
use_sip_api_v2()

from version import __version__

from PyQt4.QtCore import QSysInfo
from PyQt4.QtGui import QFont

if hasattr(QSysInfo, 'MacintoshVersion') and QSysInfo.MacintoshVersion > QSysInfo.MV_10_8:
    # fix Mac OS X 10.9 (mavericks) font issue on Qt 4.8.5
    # https://bugreports.qt-project.org/browse/QTBUG-32789
    QFont.insertSubstitution(".Lucida Grande UI", "Lucida Grande")
