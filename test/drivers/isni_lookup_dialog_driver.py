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
from cute.matchers import named
from cute.widgets import window, QDialogDriver

from ._screen_driver import ScreenDriver
from tgit.ui.dialogs.isni_lookup_dialog import ISNILookupDialog


def isni_lookup_dialog(parent):
    return IsniLookupDialogDriver(window(ISNILookupDialog, named("isni_lookup_dialog")), parent.prober,
                                  parent.gesture_performer)


class IsniLookupDialogDriver(QDialogDriver, ScreenDriver):
    def select_first_identity(self):
        self.radio(named("_identity_0")).click()

    def accept(self):
        self._button_box().click_ok()
