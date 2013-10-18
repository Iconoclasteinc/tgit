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


class Image(object):
    OTHER = 0
    FRONT_COVER = 1
    BACK_COVER = 2

    def __init__(self, mime, data, type_=OTHER, desc=''):
        self.mime = mime
        self.data = data
        self.type = type_
        self.desc = desc

    def __repr__(self):
        data = repr(self.data[:25] + '..') if len(self.data) > 25 else self.data
        return "Image(mime=%s, type_=%s, desc=%s, data=%s)" % (self.mime, self.type, self.desc,
                                                               data)

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


class Metadata(dict):
    def __init__(self, **kwargs):
        super(Metadata, self).__init__(**kwargs)
        self._images = []

    def __missing__(self, name):
        return u''

    @property
    def images(self):
        return list(self._images)

    def imagesOfType(self, imageType):
        return [image for image in self._images if image.type == imageType]

    def addImage(self, mime, data, type_=Image.OTHER, desc=''):
        self._images.append(Image(mime, data, type_, desc))

    def removeImages(self):
        del self._images[:]

    def copy(self):
        metadata = Metadata()
        metadata.merge(self)
        return metadata

    def replace(self, other):
        self.clear()
        self.merge(other)

    def merge(self, other):
        super(Metadata, self).update(other)
        self._images[:] = other.images

    def clear(self):
        super(Metadata, self).clear()
        self.removeImages()