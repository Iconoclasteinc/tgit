# -*- coding: utf-8 -*-


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
                class Announce(object):
                    def __call__(announce, *args, **kwargs):
                        self._announce(message, *args, **kwargs)

                return Announce()

        return Proxy()

    def _announce(self, message, *args, **kwargs):
        for listener in self._listeners:
            if hasattr(listener, message):
                method = getattr(listener, message)
                method(*args, **kwargs)

