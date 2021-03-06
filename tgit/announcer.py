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

import functools as func


class Announcer(object):
    def __init__(self):
        self._listeners = []

    def addListener(self, listener):
        self._listeners.append(listener)

    def removeListener(self, listener):
        if listener in self._listeners:
            self._listeners.remove(listener)

    @property
    def listeners(self):
        return list(self._listeners)

    def __getattr__(self, message):
        return func.partial(self._announce, message)

    def _announce(self, message, *args, **kwargs):
        for listener in self.listeners:
            method = getattr(listener, message)
            method(*args, **kwargs)

