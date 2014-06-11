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
from PyQt4.QtCore import QSettings


class Preferences(object):
    def __init__(self, settings):
        self.settings = settings

    def __getitem__(self, key):
        return self.settings.value(key, None)

    def __setitem__(self, key, value):
        self.settings.setValue(key, value)

    def add(self, **settings):
        for key, value in settings.iteritems():
            self[key] = value

    def keys(self):
        return self.settings.allKeys()