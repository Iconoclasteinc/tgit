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


class Contributor:
    def __init__(self, name):
        self.name = name


class ChainOfTitle:
    def __init__(self, metadata):
        self._contributors = {}
        self._publishers = {}

        contributors = set((metadata["lyricist"] or []) + (metadata["composer"] or []))
        for name in contributors:
            self._contributors[name] = Contributor(name)

        for name in metadata["publisher"] or []:
            self._publishers[name] = Contributor(name)

    @property
    def contributors(self):
        return list(self._contributors.values())

    @property
    def publishers(self):
        return list(self._publishers.values())
