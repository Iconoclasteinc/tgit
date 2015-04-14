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
    Headers = ['Album Title', 'Compilation', 'Lead Performer', 'Lead Performer ISNI', 'Guest Performers', 'Label Name',
               'Catalog Number',
               'UPC/EAN', 'Comments', 'Release Date', 'Recording Date', 'Recording Studios', 'Producer', 'Mixer',
               'Primary Style', 'Track Title', 'Version Information', 'Featured Guest', 'Lyrics', 'Language',
               'Publisher', 'Lyricist', 'Composer', 'ISRC', 'Tags']

    def __init__(self):
        QObject.__init__(self)

    def write(self, album, out):
        writer = csv.writer(out)
        self.writeHeader(writer)
        for track in album.tracks:
            self.writeRecord(writer, album, track)

    def writeHeader(self, writer):
        writer.writerow(self.encodeRow(self.Headers))

    def writeRecord(self, writer, album, track):
        row = album.releaseName, toBoolean(album.compilation), track.leadPerformer, album.isni, \
              toPeopleList(album.guestPerformers), album.labelName, album.catalogNumber, album.upc, album.comments, \
              album.releaseTime, album.recordingTime, album.recordingStudios, album.producer, \
              album.mixer, album.primaryStyle, track.trackTitle, track.versionInfo, track.featuredGuest, \
              track.lyrics, track.language, track.publisher, track.lyricist, track.composer, \
              track.isrc, track.labels
        writer.writerow(self.encodeRow(row))

    def encode(self, text):
        return text.encode(self.encoding)

    def translate(self, text):
        return text and self.tr(text) or ''

    def encodeRow(self, texts):
        return list(map(toExcelNewLines, list(map(self.translate, texts))))


def toExcelNewLines(text):
    return text.replace('\n', '\r')
