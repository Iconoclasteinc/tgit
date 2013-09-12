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

from mutagen.mp3 import MP3


class MP3File(object):
    ALBUM = 'TALB'

    def __init__(self, filename):
        super(MP3File, self).__init__()
        self.mp3 = MP3(filename)

    @property
    def album_title(self):
        return self.mp3.has_key(self.ALBUM) and self.mp3[self.ALBUM].text[0] or None

    @property
    def bitrate(self):
        return self.mp3.info.bitrate

    @property
    def bitrate_in_kbps(self):
        return int(round(self.bitrate, -3) / 1000)

    @property
    def duration(self):
        return self.mp3.info.length

    @property
    def duration_as_text(self):
        minutes, seconds = divmod(round(self.duration), 60)
        return "%02d:%02d" % (minutes, seconds)

