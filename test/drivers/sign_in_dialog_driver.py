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
from cute.matchers import named, StateMatcher
from cute.widgets import window, QDialogDriver, WidgetDriver
from tgit.ui.dialogs.sign_in_dialog import SignInDialog
from tgit.ui.widgets.progress_indicator import QProgressIndicator
from ._screen_driver import ScreenDriver


def sign_in_dialog(parent):
    return SignInDialogDriver(window(SignInDialog, named("sign_in_dialog")), parent.prober, parent.gesture_performer)


class SignInDialogDriver(QDialogDriver, ScreenDriver):
    def sign_in_with(self, username, password):
        self.enter_credentials(username, password)
        self.click_ok()

    def enter_credentials(self, username, password):
        self.enter_email(username)
        self.enter_password(password)

    def enter_email(self, username):
        self.email.replace_all_text(username)

    def enter_password(self, password):
        self.lineEdit(named("_password")).replace_all_text(password)

    def shows_authentication_failed_message(self):
        self.authentication_error.is_showing_on_screen()
        self.authentication_error.has_text("Invalid username and/or password")

    def is_showing_progress_indicator(self):
        self.progress_indicator.is_(running())

    def has_stopped_progress_indicator(self):
        self.progress_indicator.is_(stopped())

    def has_disabled_authentication(self):
        self.ok_button().is_disabled()

    def has_enabled_authentication(self):
        self.ok_button().is_enabled()

    @property
    def email(self):
        return self.lineEdit(named("_email"))

    @property
    def authentication_error(self):
        return self.label(named("_authentication_error"))

    @property
    def progress_indicator(self):
        return WidgetDriver.find_single(self, QProgressIndicator, named("_progress_indicator"))


def running():
    return StateMatcher(QProgressIndicator.isRunning, "running", "stopped")


def stopped():
    return StateMatcher(QProgressIndicator.isStopped, "stopped", "running")


