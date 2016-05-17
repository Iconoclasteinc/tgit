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
from datetime import datetime
import os
import uuid

from xml.etree import ElementTree


class FileHeader:
    def __init__(self, filename):
        self._filename = filename

    def write_to(self, root):
        header_element = ElementTree.SubElement(root, "FileHeader")
        file_id_element = ElementTree.SubElement(header_element, "FileId")
        file_id_element.text = str(uuid.uuid4())
        file_created_datetime_element = ElementTree.SubElement(header_element, "FileCreatedDateTime")
        file_created_datetime_element.text = datetime.utcnow().isoformat()
        file_name_element = ElementTree.SubElement(header_element, "FileName")
        file_name_element.text = os.path.basename(self._filename)


class Party:
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
        party_element = ElementTree.SubElement(root, "Party")

        party_reference = ElementTree.SubElement(party_element, "PartyReference")
        party_reference.text = self.reference

        if self._isni:
            party_id = ElementTree.SubElement(party_element, "PartyId", IsISNI=str(True).lower())
            isni = ElementTree.SubElement(party_id, "ISNI")
            isni.text = self._isni

        party_name = ElementTree.SubElement(party_element, "PartyName")
        full_name = ElementTree.SubElement(party_name, "FullName")
        full_name.text = self._full_name

        is_organization = ElementTree.SubElement(party_element, "IsOrganization")
        is_organization.text = str(self._is_organisation)


class PartyList:
    def __init__(self, parties):
        self._parties = parties

    def write_to(self, root):
        party_list_element = ElementTree.SubElement(root, "PartyList")
        for party in self._parties.values():
            party.write_to(party_list_element)

    def reference_for(self, name):
        return self._parties[name].reference if name in self._parties else None

    @classmethod
    def from_(cls, project):
        def add_party(name, is_organization=False):
            if name and name not in parties:
                parties[name] = Party(len(parties), name, isnis.get(name), is_organization)

        isnis = project.isnis or {}

        parties = {}
        add_party(project.lead_performer)
        add_party(project.label_name, is_organization=True)
        for _, musician in project.guest_performers or []:
            add_party(musician)

        for track in project.tracks:
            add_party(track.lead_performer)
            add_party(track.featured_guest)
            add_party(track.music_producer)
            add_party(track.mixer)
            add_party(track.recording_studio, is_organization=True)
            add_party(track.production_company, is_organization=True)
            for lyricist in track.lyricist or []:
                add_party(lyricist)
            for composer in track.composer or []:
                add_party(composer)
            for publisher in track.publisher or []:
                add_party(publisher, is_organization=True)

        return cls(parties)


class MusicalWork:
    """
    Supported : ISWC, Title, Lyrics, Comment
    Not Supported : AlternateTitle, CreationDate, MusicalWorkType
    """

    def __init__(self, track, party_list):
        self._party_list = party_list
        self._track = track

    def write_to(self, root):
        musical_work = ElementTree.SubElement(root, "MusicalWork")
        if self._track.iswc:
            musical_work_id = ElementTree.SubElement(musical_work, "MusicalWorkId")
            iswc = ElementTree.SubElement(musical_work_id, "ISWC")
            iswc.text = self._track.iswc

        if self._track.track_title:
            title = ElementTree.SubElement(musical_work, "Title")
            title.attrib["TitleType"] = "DisplayTitle"  # todo validate hypothesis
            title_text = ElementTree.SubElement(title, "TitleText")
            title_text.text = self._track.track_title

        if self._track.lyrics:
            lyrics = ElementTree.SubElement(musical_work, "Lyrics")
            lyrics.text = self._track.lyrics

        if self._track.comments:
            comments = ElementTree.SubElement(musical_work, "Comment")
            comments.text = self._track.comments

        lyricists = set(self._track.lyricist or [])
        composers = set(self._track.composer or [])
        publishers = set(self._track.publisher or [])

        for name in lyricists - composers:
            contributor = ElementTree.SubElement(musical_work, "MusicalWorkContributorReference")
            contributor_reference = ElementTree.SubElement(contributor, "MusicalWorkContributorReference")
            contributor_reference.text = self._party_list.reference_for(name)
            contributor_role = ElementTree.SubElement(contributor, "MusicalWorkContributorRole")
            contributor_role.text = "Lyricist"

        for name in composers - lyricists:
            contributor = ElementTree.SubElement(musical_work, "MusicalWorkContributorReference")
            contributor_reference = ElementTree.SubElement(contributor, "MusicalWorkContributorReference")
            contributor_reference.text = self._party_list.reference_for(name)
            contributor_role = ElementTree.SubElement(contributor, "MusicalWorkContributorRole")
            contributor_role.text = "Composer"

        for name in composers.intersection(lyricists):
            contributor = ElementTree.SubElement(musical_work, "MusicalWorkContributorReference")
            contributor_reference = ElementTree.SubElement(contributor, "MusicalWorkContributorReference")
            contributor_reference.text = self._party_list.reference_for(name)
            contributor_role = ElementTree.SubElement(contributor, "MusicalWorkContributorRole")
            contributor_role.text = "ComposerLyricist"

        for name in publishers:
            contributor = ElementTree.SubElement(musical_work, "MusicalWorkContributorReference")
            contributor_reference = ElementTree.SubElement(contributor, "MusicalWorkContributorReference")
            contributor_reference.text = self._party_list.reference_for(name)
            contributor_role = ElementTree.SubElement(contributor, "MusicalWorkContributorRole")
            contributor_role.text = "OriginalPublisher"  # todo validate hypothesis


class MusicalWorkList:
    def __init__(self, works):
        self._works = works

    def write_to(self, root):
        musical_work_list_element = ElementTree.SubElement(root, "MusicalWorkList")
        for work in self._works:
            work.write_to(musical_work_list_element)

    @classmethod
    def from_(cls, project, party_list):
        return cls([MusicalWork(track, party_list) for track in project.tracks])
