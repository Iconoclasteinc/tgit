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
    return " ".join(region) if region else ""


def _get_isni_of_identity(identity, isnis):
    return isnis[identity] if isnis and identity in isnis else ""


class CsvFormat(QObject):
    Headers = ["Release Name", "Compilation", "Lead Performer", "Lead Performer ISNI", "Lead Performer Origin",
               "Lead Performer Date of Birth", "Guest Performers", "Label Name", "Catalog Number", "UPC/EAN",
               "Comments", "Release Date", "Recording Date", "Recording Studio", "Recording Studio Address",
               "Recording Location", "Production Company", "Production Location", "Music Producer", "Mixer",
               "Primary Style", "Track Title", "Version Information", "Track Number", "Total Tracks", "Featured Guest",
               "Lyrics", "Language", "ISRC", "Tags"]

    def __init__(self):
        super().__init__()

    def write(self, album, out):
        writer = csv.writer(out)
        self._write_header(writer)
        for track in album.tracks:
            self._write_record(writer, album, track)

    def _write_header(self, writer):
        writer.writerow(self._encode_row(self._headers))

    def _write_record(self, writer, project, track):
        main_artist_isni = _get_isni_of_identity(track.lead_performer, project.isnis)
        main_artist_region = _to_standard_region_code(project.lead_performer_region)
        production_company_region = _to_standard_region_code(track.production_company_region)
        recording_studio_region = _to_standard_region_code(track.recording_studio_region)
        guest_performers = _to_people_list(project.guest_performers)
        compilation = to_boolean(project.compilation)
        track_number = str(track.track_number)
        total_tracks = str(track.total_tracks)

        row = [project.release_name, compilation, track.lead_performer, main_artist_isni, main_artist_region,
               project.lead_performer_date_of_birth, guest_performers, project.label_name, project.catalog_number,
               project.upc, track.comments, project.release_time, track.recording_time, track.recording_studio,
               recording_studio_region, track.production_company, production_company_region, track.music_producer,
               track.mixer, track.primary_style, track.track_title, track.version_info, track_number, total_tracks,
               track.featured_guest, track.lyrics, track.language, track.isrc, track.labels]

        writer.writerow(self._encode_row(row))

    @property
    def _headers(self):
        return [self.tr(header) for header in self.Headers]

    def _encode_row(self, texts):
        return [self._to_excel_new_lines(text) for text in texts]

    @staticmethod
    def _to_excel_new_lines(text):
        return text and text.replace("\n", "\r") or ""
