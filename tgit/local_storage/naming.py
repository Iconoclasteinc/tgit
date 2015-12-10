# -*- coding: utf-8 -*-
#
# TGiT, Music Tagger for Professionals
# Copyright (C) 2013 Iconoclaste Musique Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.qp6
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

from tgit import fs


def itunes_naming_scheme(track):
    return fs.sanitize(
        "{artist} - {number:02} - {title}{ext}".format(artist=track.lead_performer[0] if track.lead_performer else "",
                                                       number=track.track_number,
                                                       title=track.track_title,
                                                       ext=fs.ext(track.filename)))


def picture_naming_scheme(image):
    desc = image.desc or "Front Cover"
    return fs.sanitize("{desc}{ext}".format(desc=desc, ext=fs.guess_extension(image.mime)))


track_scheme = itunes_naming_scheme
artwork_scheme = picture_naming_scheme
