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


def to_boolean(value):
    return value and "True" or "False"


def _to_people_list(people):
    return people and "; ".join(["{0}: {1}".format(role, name) for role, name in people]) or ""


def _to_standard_region_code(region):
    return "-".join(region) if region else ""


class CsvFormat(QObject):
    Headers = "Release Name", "Compilation", "Lead Performer", "Lead Performer ISNI", "Lead Performer Region", \
              "Guest Performers", "Label Name", "Catalog Number", "UPC/EAN", "Comments", "Release Date", \
              "Recording Date", "Recording Studios", "Recording Studio Region", "Production Company", "Production Company Region", \
              "Music Producer", "Mixer", "Primary Style", "Track Title", "Version Information", "Track Number", \
              "Total Tracks", "Featured Guest", "Lyrics", "Language", "Publisher", "Lyricist", "Composer", "ISRC", \
              "Tags"

    def __init__(self):
        super().__init__()

    def write(self, album, out):
        writer = csv.writer(out)
        self._write_header(writer)
        for track in album.tracks:
            self._write_record(writer, album, track)

    def _write_header(self, writer):
        writer.writerow(self._encode_row(self._translate_texts(CsvFormat.Headers)))

    def _write_record(self, writer, album, track):
        lead_performer_region = _to_standard_region_code(album.lead_performer_region)
        production_company_region = _to_standard_region_code(album.production_company_region)
        recording_studio_region = _to_standard_region_code(album.recording_studio_region)
        guest_performers = _to_people_list(album.guest_performers)
        compilation = to_boolean(album.compilation)
        track_number = str(track.track_number)
        total_tracks = str(track.total_tracks)

        row = (
            album.release_name, compilation, track.lead_performer, album.isni, lead_performer_region, guest_performers,
            album.label_name,
            album.catalog_number, album.upc, album.comments, album.release_time, album.recording_time,
            album.recording_studios, recording_studio_region, album.production_company, production_company_region,
            album.music_producer, album.mixer,
            album.primary_style, track.track_title,
            track.versionInfo, track_number, total_tracks, track.featuredGuest, track.lyrics, track.language,
            track.publisher, track.lyricist, track.composer, track.isrc, track.labels)

        writer.writerow(self._encode_row(row))

    def _translate(self, text):
        return text and self.tr(text) or ""

    def _translate_texts(self, texts):
        return map(self._translate, texts)

    def _encode_row(self, texts):
        return list(map(self.to_excel_new_lines, texts))

    @staticmethod
    def to_excel_new_lines(text):
        return text and text.replace("\n", "\r") or ""
