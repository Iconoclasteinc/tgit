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
        instance.signalStateChange()


class typed(tag):
    expectedType = type(None)

    def __set__(self, instance, value):
        if not isinstance(value, self.expectedType):
            raise TypeError('expected {}, not {}'.format(self.expectedType, type(value)))
        super(typed, self).__set__(instance, value)


class integer(typed):
    expectedType = int


class text(typed):
    expectedType = (str, unicode)


class decimal(typed):
    expectedType = (int, float)


class boolean(typed):
    expectedType = bool


class Taggable(type):
    def __new__(cls, clsname, bases, methods):
        # Attach attribute names to the tags
        for key, value in methods.items():
            if isinstance(value, tag):
                value.name = key
        return type.__new__(cls, clsname, bases, methods)

    def tags(cls):
        return (value.name for value in cls.__dict__.itervalues() if isinstance(value, tag))


# todo move tags to album.py

FRONT_COVER = 'frontCover'

RELEASE_NAME = 'releaseName'
LEAD_PERFORMER = 'leadPerformer'
GUEST_PERFORMERS = 'guestPerformers'
LABEL_NAME = 'labelName'
UPC = 'upc'
CATALOG_NUMBER = 'catalogNumber'
RELEASE_TIME = 'releaseTime'
ORIGINAL_RELEASE_TIME = 'originalReleaseTime'
RECORDING_TIME = 'recordingTime'
RECORDING_STUDIOS = 'recordingStudios'
PRODUCER = 'producer'
MIXER = 'mixer'
CONTRIBUTORS = 'contributors'
COMMENTS = 'comments'
PRIMARY_STYLE = 'primaryStyle'
COMPILATION = 'compilation'


ALBUM_TAGS = [
    RELEASE_NAME,
    COMPILATION,
    LEAD_PERFORMER,
    GUEST_PERFORMERS,
    LABEL_NAME,
    UPC,
    CATALOG_NUMBER,
    RECORDING_TIME,
    RELEASE_TIME,
    ORIGINAL_RELEASE_TIME,
    RECORDING_STUDIOS,
    PRODUCER,
    MIXER,
    CONTRIBUTORS,
    COMMENTS,
    PRIMARY_STYLE
]