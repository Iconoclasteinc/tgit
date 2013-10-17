# -*- coding: utf-8 -*-

import functools as func


class Announcer(object):
    def __init__(self):
        self._listeners = []

    def add(self, listener):
        self._listeners.append(listener)

    def remove(self, listener):
        self._listeners.remove(listener)

    def announce(self):
        class Proxy(object):
            def __getattribute__(proxy, message):
                return func.partial(self._announce, message)

        return Proxy()

    def _announce(self, message, *args, **kwargs):
        for listener in self._listeners:
            method = getattr(listener, message)
            method(*args, **kwargs)

