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
    FRONT_COVER = 3
    UTF_8 = 3

    def __init__(self, filename):
        super(MP3File, self).__init__()
        self._mp3 = MP3(filename)

    @property
    def front_cover_picture(self):
        attached_pictures = self._frames('APIC')
        for pic in attached_pictures:
            if pic.type == MP3File.FRONT_COVER:
                return pic.data

        return None

    @front_cover_picture.setter
    def front_cover_picture(self, picture):
        mime_type, image_data = picture
        front_cover = id3.APIC(encoding=MP3File.UTF_8, mime=mime_type, type=MP3File.FRONT_COVER,
                               desc='Front Cover', data=image_data)
        self._overwrite_tags('APIC', front_cover)

    @property
    def release_name(self):
        return self._frame_text('TALB')

    @release_name.setter
    def release_name(self, album):
        self._add_tag(id3.TALB(encoding=MP3File.UTF_8, text=[album]))

    @property
    def lead_performer(self):
        return self._frame_text('TPE1')

    @lead_performer.setter
    def lead_performer(self, artist):
        self._add_tag(id3.TPE1(encoding=MP3File.UTF_8, text=[artist]))

    @property
    def original_release_date(self):
        return self._frame_timestamp('TDOR')

    @original_release_date.setter
    def original_release_date(self, timestamp):
        self._add_tag(id3.TDOR(encoding=MP3File.UTF_8, text=[id3.ID3TimeStamp(timestamp)]))

    @property
    def upc(self):
        return self._frame_text('TXXX:UPC')

    @upc.setter
    def upc(self, code):
        self._add_tag(id3.TXXX(encoding=MP3File.UTF_8, desc='UPC', text=[code]))

    @property
    def track_title(self):
        return self._frame_text(id3.TIT2.__name__)

    @track_title.setter
    def track_title(self, title):
        self._add_tag(id3.TIT2(encoding=MP3File.UTF_8, text=[title]))

    @property
    def version_info(self):
        return self._frame_text(id3.TPE4.__name__)

    @version_info.setter
    def version_info(self, info):
        self._add_tag(id3.TPE4(encoding=MP3File.UTF_8, text=[info]))

    @property
    def featured_guest(self):
        return self._frame_text('TXXX:Featured Guest')

    @featured_guest.setter
    def featured_guest(self, name):
        self._add_tag(id3.TXXX(encoding=MP3File.UTF_8, desc='Featured Guest', text=[name]))

    @property
    def isrc(self):
        return self._frame_text('TSRC')

    @isrc.setter
    def isrc(self, isrc):
        self._add_tag(id3.TSRC(encoding=MP3File.UTF_8, text=[isrc]))

    @property
    def bitrate(self):
        return self._mp3.info.bitrate

    @property
    def bitrate_in_kbps(self):
        return int(round(self.bitrate, -3) / 1000)

    @property
    def duration(self):
        return self._mp3.info.length

    @property
    def duration_as_text(self):
        minutes, seconds = divmod(round(self.duration), 60)
        return "%02d:%02d" % (minutes, seconds)

    def save(self):
        self._mp3.save()

    def _frame_text(self, key):
        return self._has_frame(key) and self._text(self._frame(key)) or None

    def _frame_timestamp(self, key):
        return self._has_frame(key) and self._timestamp(self._frame(key)) or None

    def _has_frame(self, key):
        return key in self._mp3.tags

    def _text(self, frame):
        return frame.text[0]

    def _timestamp(self, frame):
        return self._text(frame).text

    def _frame(self, key):
        return self._mp3[key]

    def _add_tag(self, frame):
        self._mp3.tags.add(frame)

    def _overwrite_tags(self, key, *frames):
        self._mp3.tags.setall(key, frames)

    def _frames(self, key):
        return self._mp3.tags.getall(key)