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


class tag(object):
    def __init__(self, name=None, **opts):
        self.name = name
        for key, value in opts.items():
            setattr(self, key, value)

    def __get__(self, instance, owner):
        return instance.metadata[self.name]

    def __set__(self, instance, value):
        instance.metadata[self.name] = value
        instance.metadataChanged()


class typed(tag):
    expectedType = type(None)

    def __set__(self, instance, value):
        if not isinstance(value, self.expectedType):
            raise TypeError('expected {0}, not {1}'.format(self.expectedType, type(value)))
        super(typed, self).__set__(instance, value)


class numeric(typed):
    expectedType = int


class text(typed):
    expectedType = (str, str, type(None))


class decimal(typed):
    expectedType = (int, float)


class flag(typed):
    expectedType = bool


class pairs(typed):
    expectedType = (list, tuple)


class Taggable(type):
    def __new__(cls, clsname, bases, methods):
        # Attach attribute names to the tags
        for key, value in methods.items():
            if isinstance(value, tag):
                value.name = key
        return type.__new__(cls, clsname, bases, methods)

    def tags(cls):
        return (value.name for value in cls.__dict__.values() if isinstance(value, tag))