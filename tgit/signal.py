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


# Descriptor class for signals
class signal:
    def __init__(self, type_=None, name=None):
        self.name = name
        self._type = type_

    def __get__(self, instance, owner):
        if self.name not in instance.__dict__:
            if not self._type:
                self._type = type(instance)
            instance.__dict__[self.name] = Signal(self.name, self._type)
        return instance.__dict__[self.name]


class Observable(type):
    def __new__(mcs, clsname, bases, methods):
        # Attach names to the signals
        for key, value in methods.items():
            if isinstance(value, signal) and not value.name:
                value.name = key
        return super().__new__(mcs, clsname, bases, methods)


class Signal:
    def __init__(self, name, type_):
        self._name = name
        self._type = type_
        self._subscribers = []

    def emit(self, event):
        if not isinstance(event, self._type):
            raise TypeError("{} event should be of type {}, not {}".format(
                self._name, self._type.__name__, type(event).__name__))

        for subscriber in self._subscribers:
            subscriber(event)

    def subscribe(self, subscriber):
        if not callable(subscriber):
            raise TypeError("Subscriber does not seem callable: " + type(subscriber).__name__)

        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        if subscriber in self._subscribers:
            self._subscribers.remove(subscriber)