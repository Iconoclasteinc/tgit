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

from PyQt5.QtCore import QSettings
from preferences import Preferences

from tgit.audio import MediaPlayer
from tgit.tagger import TGiT
from tgit.isni.name_registry import NameRegistry


def main():
    name_registry = NameRegistry(host="isni-m.oclc.nl",
                                 assign_host="isni-m-acc.oclc.nl",
                                 secure=True,
                                 username="ICON",
                                 password="crmeoS4d")

    app = TGiT(MediaPlayer, name_registry)
    app.setApplicationName("TGiT")
    app.setOrganizationName("Iconoclaste Inc.")
    app.setOrganizationDomain("tagyourmusic.com")
    app.launch(Preferences(QSettings()))


if __name__ == "__main__":
    main()