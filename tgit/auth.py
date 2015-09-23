# -*- coding: utf-8 -*-
from enum import Enum

from tgit.signal import Observable
from tgit.signal import signal


class Permission(Enum):
    isni_lookup = range(1)


class User():
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
    def registered(self):
        return self._email is not None

    def has_permission(self, permission):
        return self.registered


class Session(metaclass=Observable):
    user_signed_in = signal(User)
    user_signed_out = signal(User)

    _user = User.anonymous()

    def login_as(self, email, token):
        self._user = User.registered_as(email, token)
        self.user_signed_in.emit(self._user)

    def logout(self):
        logged_out = self._user
        self._user = User.anonymous()
        self.user_signed_out.emit(logged_out)

    @property
    def current_user(self):
        return self._user
