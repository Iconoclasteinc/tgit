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

from xml.etree import ElementTree


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
            title.attrib["TitleType"] = "FormalTitle"  # todo validate hypothesis
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
        sequence = 0

        for name in lyricists - composers:
            contributor = ElementTree.SubElement(musical_work, "MusicalWorkContributorReference")
            contributor.attrib["Sequence"] = str(sequence)
            contributor_reference = ElementTree.SubElement(contributor, "MusicalWorkContributorReference")
            contributor_reference.text = self._party_list.reference_for(name)
            contributor_role = ElementTree.SubElement(contributor, "MusicalWorkContributorRole")
            contributor_role.text = "Lyricist"
            sequence += 1

        for name in composers - lyricists:
            contributor = ElementTree.SubElement(musical_work, "MusicalWorkContributorReference")
            contributor.attrib["Sequence"] = str(sequence)
            contributor_reference = ElementTree.SubElement(contributor, "MusicalWorkContributorReference")
            contributor_reference.text = self._party_list.reference_for(name)
            contributor_role = ElementTree.SubElement(contributor, "MusicalWorkContributorRole")
            contributor_role.text = "Composer"
            sequence += 1

        for name in composers.intersection(lyricists):
            contributor = ElementTree.SubElement(musical_work, "MusicalWorkContributorReference")
            contributor.attrib["Sequence"] = str(sequence)
            contributor_reference = ElementTree.SubElement(contributor, "MusicalWorkContributorReference")
            contributor_reference.text = self._party_list.reference_for(name)
            contributor_role = ElementTree.SubElement(contributor, "MusicalWorkContributorRole")
            contributor_role.text = "ComposerLyricist"
            sequence += 1

        for name in publishers:
            contributor = ElementTree.SubElement(musical_work, "MusicalWorkContributorReference")
            contributor.attrib["Sequence"] = str(sequence)
            contributor_reference = ElementTree.SubElement(contributor, "MusicalWorkContributorReference")
            contributor_reference.text = self._party_list.reference_for(name)
            contributor_role = ElementTree.SubElement(contributor, "MusicalWorkContributorRole")
            contributor_role.text = "OriginalPublisher"  # todo validate hypothesis
            sequence += 1


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
