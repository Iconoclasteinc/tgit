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


def sign_in(login, authenticator):
    def sign_in_with(email, password):
        try:
            user = authenticator.authenticate(email, password)
            login.authentication_succeeded(user["email"], user["token"], user["permissions"])
        except Exception as error:
            login.authentication_failed(error)

    return sign_in_with


class Login(metaclass=Observable):
    login_successful = signal(str)
    login_failed = signal(Exception)

    def __init__(self, session):
        self._session = session

    def authentication_succeeded(self, email, token, permissions):
        self._session.login_as(email, token, permissions)
        self.login_successful.emit(email)

    def authentication_failed(self, error):
        self.login_failed.emit(error)


class Permission(Enum):
    lookup_isni = "isni.lookup"
    assign_isni = "isni.assign"


class User:
    @classmethod
    def anonymous(cls):
        return cls()

    @classmethod
    def registered_as(cls, email, api_token, permissions):
        return cls(email, api_token, permissions)

    def __init__(self, email=None, api_key=None, permissions=None):
        self._email = email
        self._api_key = api_key
        # todo this should be Permissions, not their values
        self._permissions = permissions

    @property
    def email(self):
        return self._email

    @property
    def api_key(self):
        return self._api_key

    @property
    def permissions(self):
        return self._permissions

    @property
    def registered(self):
        return self._email is not None

    def has_permission(self, permission):
        return self.registered and permission.value in self._permissions


class Session(metaclass=Observable):
    user_signed_in = signal(User)
    user_signed_out = signal(User)

    _user = None

    def login_as(self, email, token, permissions):
        self._user = User.registered_as(email, token, permissions)
        self.user_signed_in.emit(self._user)

    def logout(self):
        logged_out, self._user = self._user, None
        self.user_signed_out.emit(logged_out)

    @property
    def opened(self):
        return self._user is not None

    @property
    def current_user(self):
        return self._user if self.opened else User.anonymous()
