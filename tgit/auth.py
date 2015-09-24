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

from enum import Enum

from tgit.signal import Observable
from tgit.signal import signal


class Permission(Enum):
    isni_lookup = range(1)


class User:
    @classmethod
    def anonymous(cls):
        return cls()

    @classmethod
    def registered_as(cls, email, api_token):
        return cls(email, api_token)

    def __init__(self, email=None, api_key=None):
        self._email = email
        self._api_key = api_key

    @property
    def email(self):
        return self._email

    @property
    def api_key(self):
        return self._api_key

    @property
    def registered(self):
        return self._email is not None

    def has_permission(self, permission):
        return self.registered


class Session(metaclass=Observable):
    user_signed_in = signal(User)
    user_signed_out = signal(User)

    _user = None

    def login_as(self, email, token):
        self._user = User.registered_as(email, token)
        self.user_signed_in.emit(self._user)

    def logout(self):
        logged_out = self._user
        self._user = None
        self.user_signed_out.emit(logged_out)

    @property
    def opened(self):
        return self._user is not None

    @property
    def current_user(self):
        return self.opened and self._user or User.anonymous()
