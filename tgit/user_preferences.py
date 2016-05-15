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

from tgit.signal import Observable, signal
from tgit.ui import locations


def load_from(settings):
    prefs = settings.load_preferences()
    prefs.on_preferences_changed.subscribe(lambda change: settings.store_preferences(prefs))
    return prefs


class UserPreferences(metaclass=Observable):
    on_preferences_changed = signal(dict)

    artwork_location = locations.Pictures
    export_location = locations.Documents
    locale = "en"

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        self.on_preferences_changed.emit({name: value})

    def __repr__(self):
        return "UserPreferences(locale={})".format(self.locale)
