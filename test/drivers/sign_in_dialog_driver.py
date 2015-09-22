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
from tgit.ui.sign_in_dialog import SignInDialog


def sign_in_dialog(parent):
    return SignInDialogDriver(window(SignInDialog, named("sign_in_dialog")), parent.prober, parent.gesture_performer)


class SignInDialogDriver(QDialogDriver, ScreenDriver):
    def enter_credentials(self, username, password):
        self.lineEdit(named("_email")).replace_all_text(username)
        self.lineEdit(named("_password")).replace_all_text(password)
        self.ok()

    def shows_authentication_failed_message(self):
        self.label(named("_authentication_error")).is_showing_on_screen()
        self.label(named("_authentication_error")).has_text("Incorrect username and/or password.")
