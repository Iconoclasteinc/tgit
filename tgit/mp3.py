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
    FEATURED_GUEST = 'Featured Guest'
    UPC = 'UPC'

    FRONT_COVER = 3
    UTF_8 = 3

    def __init__(self, filename):
        super(MP3File, self).__init__()
        self._mp3 = MP3(filename)

    @property
    def front_cover_picture(self):
        attached_pictures = self._frames_of_type(id3.APIC)
        for pic in attached_pictures:
            if pic.type == MP3File.FRONT_COVER:
                return pic.mime, pic.data

        return None, None

    @front_cover_picture.setter
    def front_cover_picture(self, picture):
        mime_type, image_data = picture
        if image_data is None:
            self._overwrite_frames(id3.APIC)
            return
        front_cover = id3.APIC(encoding=MP3File.UTF_8, mime=mime_type, type=MP3File.FRONT_COVER,
                               desc='Front Cover', data=image_data)
        self._overwrite_frames(id3.APIC, front_cover)

    @property
    def release_name(self):
        return self._get_text(id3.TALB())

    @release_name.setter
    def release_name(self, album):
        self._add_text_frame(id3.TALB(text=album))

    @property
    def lead_performer(self):
        return self._get_text(id3.TPE1())

    @lead_performer.setter
    def lead_performer(self, artist):
        self._add_text_frame(id3.TPE1(text=artist))

    @property
    def original_release_date(self):
        return self._get_text(id3.TDOR())

    @original_release_date.setter
    def original_release_date(self, timestamp):
        self._add_text_frame(id3.TDOR(text=timestamp))

    @property
    def upc(self):
        return self._get_text(id3.TXXX(desc=MP3File.UPC))

    @upc.setter
    def upc(self, code):
        self._add_text_frame(id3.TXXX(desc=MP3File.UPC, text=code))

    @property
    def track_title(self):
        return self._get_text(id3.TIT2())

    @track_title.setter
    def track_title(self, title):
        self._add_text_frame(id3.TIT2(text=title))

    @property
    def version_info(self):
        return self._get_text(id3.TPE4())

    @version_info.setter
    def version_info(self, info):
        self._add_text_frame(id3.TPE4(text=info))

    @property
    def featured_guest(self):
        return self._get_text(id3.TXXX(desc=MP3File.FEATURED_GUEST))

    @featured_guest.setter
    def featured_guest(self, name):
        self._add_text_frame(id3.TXXX(desc=MP3File.FEATURED_GUEST, text=name))

    @property
    def isrc(self):
        return self._get_text(id3.TSRC())

    @isrc.setter
    def isrc(self, isrc):
        self._add_text_frame(id3.TSRC(text=isrc))

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

    def _get_text(self, frame):
        return self._has_frame(frame) and self._as_text(frame) or None

    def _has_frame(self, frame):
        return frame.HashKey in self._mp3.tags

    def _as_text(self, frame):
        return unicode(self._mp3[frame.HashKey])

    def _add_text_frame(self, frame):
        frame.encoding = MP3File.UTF_8
        self._add_frame(frame)

    def _add_frame(self, frame):
        self._mp3.tags.add(frame)

    def _overwrite_frames(self, frame_type, *frames):
        self._mp3.tags.setall(self._frame_id(frame_type), frames)

    def _frames_of_type(self, frame_type):
        return self._mp3.tags.getall(self._frame_id(frame_type))

    def _frame_id(self, frame_type):
        return frame_type.__name__
