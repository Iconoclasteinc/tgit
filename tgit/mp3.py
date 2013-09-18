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


RELEASE_NAME = id3.TALB
LEAD_PERFORMER = id3.TPE1
TRACK_TITLE = id3.TIT2
VERSION_INFO = id3.TPE4
ATTACHED_PICTURE = id3.APIC

FRONT_COVER_PICTURE = 3
UTF_8 = 3


def name_of(frame):
    return frame.__name__


class MP3File(object):
    def __init__(self, filename):
        super(MP3File, self).__init__()
        self.mp3 = MP3(filename)

    @property
    def release_name(self):
        return self._get_frame_text(RELEASE_NAME)

    @release_name.setter
    def release_name(self, album):
        self._set_frame_text(RELEASE_NAME, album)

    @property
    def front_cover_picture(self):
        attached_pictures = self._get_all(ATTACHED_PICTURE)
        for pic in attached_pictures:
            if pic.type == FRONT_COVER_PICTURE:
                return pic.data

        return None

    @front_cover_picture.setter
    def front_cover_picture(self, picture):
        self._set_frame(self._image_frame(mime_type=picture[0],
                                          type=FRONT_COVER_PICTURE,
                                          description='Front Cover',
                                          image_data=picture[1]))

    @property
    def lead_performer(self):
        return self._get_frame_text(LEAD_PERFORMER)

    @lead_performer.setter
    def lead_performer(self, artist):
        self._set_frame_text(LEAD_PERFORMER, artist)

    @property
    def track_title(self):
        return self._get_frame_text(TRACK_TITLE)

    @track_title.setter
    def track_title(self, track):
        self._set_frame_text(TRACK_TITLE, track)

    @property
    def version_info(self):
        return self._get_frame_text(VERSION_INFO)

    @version_info.setter
    def version_info(self, info):
        self._set_frame_text(VERSION_INFO, info)

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
        return self._has_frame(frame) and self._is_text_frame(frame) and self._text_of(frame) or \
            None

    def _has_frame(self, frame):
        return self.mp3.has_key(name_of(frame))

    def _is_text_frame(self, frame):
        return self.mp3[name_of(frame)].__dict__.has_key('text')

    def _text_of(self, frame):
        return self.mp3[name_of(frame)][0]

    def _set_frame_text(self, frame, text):
        self._set_frame(self._text_frame(frame, text))

    def _text_frame(self, frame, text):
        return frame(encoding=UTF_8, text=text)

    def _set_frame(self, frame):
        self.mp3.tags.setall(name_of(type(frame)), [frame])

    def _get_all(self, frame):
        return self.mp3.tags.getall(name_of(frame))

    def _image_frame(self, mime_type, type, description, image_data):
        return ATTACHED_PICTURE(encoding=UTF_8,
                                mime=mime_type,
                                type=type,
                                desc=description,
                                data=image_data)
