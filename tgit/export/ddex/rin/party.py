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

from tgit.export.ddex.rin.section import Section


class Party(Section):
    """
    Supported: PartyId (ISNI), FullName, IsOrganization
    Not Supported:
        FullNameAsciiTranscribed, FullNameIndexed, NamesBeforeKeyName, KeyName, NamesAfterKeyName, AbbreviatedName,
        PostalAddress, PhoneNumber, EmailAddress, Nationality
    """

    def __init__(self, sequence, full_name, isni=None, is_organization=False):
        self._sequence = sequence
        self._is_organisation = str(is_organization).lower()
        self._isni = isni
        self._full_name = full_name

    @property
    def reference(self):
        return "P-{0:05d}".format(self._sequence)

    def write_to(self, root):
        party = self._build_sub_element(root, "Party")
        self._build_sub_element(party, "PartyReference", self.reference)
        self._build_sub_element(party, "IsOrganization", str(self._is_organisation))
        self._build_party_id(party)
        self._build_party_name(party)

    def _build_party_name(self, party):
        party_name = self._build_sub_element(party, "PartyName")
        self._build_sub_element(party_name, "FullName", self._full_name)

    def _build_party_id(self, parent):
        if self._isni:
            party_id = self._build_sub_element(parent, "PartyId", IsISNI=str(True).lower())
            self._build_sub_element(party_id, "ISNI", self._isni)


class PartyList(Section):
    def __init__(self, parties):
        self._parties = parties

    def write_to(self, root):
        party_list = self._build_sub_element(root, "PartyList")
        for party in self._parties.values():
            party.write_to(party_list)

    def reference_for(self, name):
        return self._parties[name].reference if name in self._parties else None

    @classmethod
    def from_(cls, project):
        def append_party(name, is_organization=False):
            if name and name not in parties:
                parties[name] = Party(len(parties), name, project.isnis.get(name), is_organization)

        def append_track_parties(track):
            append_party(track.lead_performer)
            append_party(track.featured_guest)
            append_party(track.music_producer)
            append_party(track.mixer)
            append_party(track.recording_studio, is_organization=True)
            append_party(track.production_company, is_organization=True)
            for lyricist in track.lyricist:
                append_party(lyricist)
            for composer in track.composer:
                append_party(composer)
            for publisher in track.publisher:
                append_party(publisher, is_organization=True)

        def append_project_parties():
            append_party(project.lead_performer)
            append_party(project.label_name, is_organization=True)
            for _, musician in project.guest_performers:
                append_party(musician)

        parties = {}
        append_project_parties()
        for each_track in project.tracks:
            append_track_parties(each_track)

        return cls(parties)
