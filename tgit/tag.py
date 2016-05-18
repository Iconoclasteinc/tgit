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

from tgit.signal import Observable, signal, Signal


class Tag:
    name = None
    _default_value = None

    def __get__(self, instance, owner):
        return instance.metadata.get(self.name, self._default_value)

    def __set__(self, instance, value):
        old_value = instance.metadata[self.name]
        if old_value != value:
            instance.metadata[self.name] = value
            instance.metadata_changed.emit(instance)


class Typed(Tag):
    _expected_type = type(None)

    def __set__(self, instance, value):
        if not isinstance(value, self._expected_type):
            raise TypeError("expected {}, not {}".format(self._expected_type, type(value)))
        super(Typed, self).__set__(instance, value)


class numeric(Typed):
    _expected_type = int
    _default_value = 0


class text(Typed):
    _expected_type = (str, type(None))
    _default_value = ""


class decimal(Typed):
    _expected_type = (int, float)
    _default_value = 0


class flag(Typed):
    _expected_type = (bool, type(None))


class pairs(Typed):
    _expected_type = (list, tuple, type(None))
    _default_value = []


class sequence(Typed):
    _expected_type = (list, type(None))
    _default_value = []


class map(Typed):
    _expected_type = (dict, type(None))
    _default_value = {}


class Taggable(Observable):
    def __new__(mcs, clsname, bases, methods):
        methods["metadata_changed"] = signal(Signal.SELF)

        # Attach attribute names to the tags
        for key, value in methods.items():
            if isinstance(value, Tag):
                value.name = key
        return super().__new__(mcs, clsname, bases, methods)

    def tags(cls):
        return (value.name for value in cls.__dict__.values() if isinstance(value, Tag))
