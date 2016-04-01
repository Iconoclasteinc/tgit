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

from PyQt5.QtGui import QPixmap, QImage

from tgit import imager
from tgit.metadata import Image
from tgit.ui import resources

INVALID_IMAGE = Image("image/png", resources.load(":/images/broken"))
PLACEHOLDER_IMAGE = Image("image/png", resources.load(":/images/placeholder"))


def broken(width, height):
    return from_image(imager.scale(INVALID_IMAGE, width, height))


def none(width, height):
    return from_image(imager.scale(PLACEHOLDER_IMAGE, width, height))


def from_image(image):
    return QPixmap.fromImage(QImage.fromData(image.data))
