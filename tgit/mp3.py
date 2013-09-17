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
from mutagen import id3


class MP3File(object):
    ALBUM_TITLE = id3.TALB
    ALBUM_ARTIST = id3.TPE1
    TRACK_TITLE = id3.TIT2
    VERSION_INFO = id3.TPE4

    def __init__(self, filename):
        super(MP3File, self).__init__()
        self.mp3 = MP3(filename)

    @property
    def album_title(self):
        return self._get_frame_text(MP3File.ALBUM_TITLE)

    @album_title.setter
    def album_title(self, album):
        self._set_frame_text(MP3File.ALBUM_TITLE, album)

    @property
    def album_artist(self):
        return self._get_frame_text(MP3File.ALBUM_ARTIST)

    @album_artist.setter
    def album_artist(self, artist):
        self._set_frame_text(MP3File.ALBUM_ARTIST, artist)

    @property
    def track_title(self):
        return self._get_frame_text(MP3File.TRACK_TITLE)

    @track_title.setter
    def track_title(self, track):
        self._set_frame_text(MP3File.TRACK_TITLE, track)

    @property
    def version_info(self):
        return self._get_frame_text(MP3File.VERSION_INFO)

    @version_info.setter
    def version_info(self, info):
        self._set_frame_text(MP3File.VERSION_INFO, info)

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

    def save(self):
        self.mp3.save()

    def _get_frame_text(self, frame):
        return self.mp3.has_key(frame.__name__) and self.mp3[frame.__name__].text[0] or None

    def _set_frame_text(self, frame, text):
        self.mp3.tags.add(frame(encoding=3, text=text))

