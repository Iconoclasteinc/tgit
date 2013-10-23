# -*- coding: utf-8 -*-

import functools as func


class Announcer(object):
    def __init__(self):
        self._listeners = []

    def addListener(self, listener):
        self._listeners.append(listener)

    def removeListener(self, listener):
        self._listeners.remove(listener)

    def __getattr__(self, message):
        return func.partial(self._announce, message)

    def _announce(self, message, *args, **kwargs):
        for listener in self._listeners:
            if hasattr(listener, message):
                method = getattr(listener, message)
                method(*args, **kwargs)

