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

from tgit.signal import Observable


class Tag:
    name = None

    def __get__(self, instance, owner):
        return instance.metadata[self.name]

    def __set__(self, instance, value):
        instance.metadata[self.name] = value
        instance.metadataChanged()


class Typed(Tag):
    _expected_type = type(None)

    def __set__(self, instance, value):
        if not isinstance(value, self._expected_type):
            raise TypeError("expected {0}, not {1}".format(self._expected_type, type(value)))
        super(Typed, self).__set__(instance, value)


class numeric(Typed):
    _expected_type = int


class text(Typed):
    _expected_type = (str, type(None))


class decimal(Typed):
    _expected_type = (int, float)


class flag(Typed):
    _expected_type = (bool, type(None))


class pairs(Typed):
    _expected_type = (list, tuple, type(None))


class map(Typed):
    _expected_type = (dict, type(None))


class Taggable(Observable):
    def __new__(mcs, clsname, bases, methods):
        # Attach attribute names to the tags
        for key, value in methods.items():
            if isinstance(value, Tag):
                value.name = key
        return super().__new__(mcs, clsname, bases, methods)

    def tags(cls):
        return (value.name for value in cls.__dict__.values() if isinstance(value, Tag))
