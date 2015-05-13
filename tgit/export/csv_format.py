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

import csv

from PyQt5.QtCore import QObject


def toBoolean(value):
    return value and 'True' or 'False'


def toPeopleList(people):
    return people and '; '.join(['%s: %s' % (role, name) for role, name in people]) or ''


class CsvFormat(QObject):
    Headers = 'Release Name', 'Compilation', 'Lead Performer', 'Lead Performer ISNI', 'Guest Performers', \
              'Label Name', 'Catalog Number', 'UPC/EAN', 'Comments', 'Release Date', 'Recording Date', \
              'Recording Studios', 'Producer', 'Mixer', 'Primary Style', 'Track Title', 'Version Information', \
              'Track Number', 'Total Tracks', 'Featured Guest', 'Lyrics', 'Language', 'Publisher', 'Lyricist', \
              'Composer', 'ISRC', 'Tags'

    def __init__(self):
        QObject.__init__(self)

    def write(self, album, out):
        writer = csv.writer(out)
        self.writeHeader(writer)
        for track in album.tracks:
            self.writeRecord(writer, album, track)

    def writeHeader(self, writer):
        writer.writerow(self._encode_row(self._translate_texts(CsvFormat.Headers)))

    def writeRecord(self, writer, album, track):
        row = album.release_name, toBoolean(album.compilation), track.lead_performer, album.isni, \
              toPeopleList(album.guestPerformers), album.label_name, album.catalogNumber, album.upc, album.comments, \
              album.releaseTime, album.recording_time, album.recordingStudios, album.producer, \
              album.mixer, album.primary_style, track.track_title, track.versionInfo, str(track.track_number), \
              str(track.total_tracks), track.featuredGuest, track.lyrics, track.language, track.publisher, \
              track.lyricist, track.composer, track.isrc, track.labels
        writer.writerow(self._encode_row(row))

    def _translate(self, text):
        return text and self.tr(text) or ''

    def _translate_texts(self, texts):
        return map(self._translate, texts)

    def _encode_row(self, texts):
        return list(map(self.to_excel_new_lines, texts))

    @staticmethod
    def to_excel_new_lines(text):
        return text and text.replace('\n', '\r') or ''
