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
from PyQt5.QtCore import QLocale, QSettings

from tgit.auth import Session
from tgit.user_preferences import UserPreferences


class SettingsBackend:
    def __init__(self, file=None):
        if file:
            self._storage = QSettings(file, QSettings.IniFormat)
        else:
            self._storage = QSettings()

    def load_session(self):
        user_email = self._storage.value("user.email", None)
        user_api_key = self._storage.value("user.api_key", None)

        session = Session()
        if user_email and user_api_key:
            session.login_as(user_email, user_api_key)

        session.user_signed_in.subscribe(self._store_user)
        session.user_signed_out.subscribe(self._remove_user)
        return session

    def load_user_preferences(self):
        preferences = UserPreferences()
        preferences.locale = QLocale(self._storage.value("preferences.locale") or "en")

        preferences.preferences_changed.subscribe(self._store_preferences)
        return preferences

    def _store_user(self, user):
        self._storage.setValue("user.email", user.email)
        self._storage.setValue("user.api_key", user.api_key)

    def _remove_user(self, user):
        self._storage.remove("user.email")
        self._storage.remove("user.api_key")

    def _store_preferences(self, preferences):
        self._storage.setValue("preferences.locale", preferences.locale.name())
