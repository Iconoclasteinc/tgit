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


class MusicalWork(Section):
    """
    Supported : ISWC, Title, Lyrics, Comment
    Not Supported : AlternateTitle, CreationDate, MusicalWorkType
    """

    def __init__(self, sequence, track, parties):
        self._sequence = sequence
        self._parties = parties
        self._track = track

    @property
    def reference(self):
        return "W-{0:05d}".format(self._sequence)

    def write_to(self, root):
        musical_work = self._build_sub_element(root, "MusicalWork")
        self._build_sub_element(musical_work, "MusicalWorkReference", self.reference)
        self._build_musical_work_id(musical_work)
        self._build_title(musical_work)
        self._build_lyrics(musical_work)
        self._build_comments(musical_work)
        self._build_contributor_references(musical_work)

    def _build_contributor_references(self, musical_work):
        track_lyricists = set(self._track.lyricist or [])
        track_composers = set(self._track.composer or [])
        publishers = set(self._track.publisher or [])

        lyricists = track_lyricists - track_composers
        composers = track_composers - track_lyricists
        composer_lyricists = track_composers.intersection(track_lyricists)

        index = self._build_contributors(lyricists, "Lyricist", musical_work, 0)
        index = self._build_contributors(composers, "Composer", musical_work, index)
        index = self._build_contributors(composer_lyricists, "ComposerLyricist", musical_work, index)
        self._build_contributors(publishers, "OriginalPublisher", musical_work, index)

    def _build_comments(self, musical_work):
        if self._track.comments:
            self._build_sub_element(musical_work, "Comment", self._track.comments)

    def _build_lyrics(self, musical_work):
        if self._track.lyrics:
            self._build_sub_element(musical_work, "Lyrics", self._track.lyrics)

    def _build_title(self, musical_work):
        if self._track.track_title:
            title = self._build_sub_element(musical_work, "Title", TitleType="FormalTitle")  # todo validate hypothesis
            self._build_sub_element(title, "TitleText", self._track.track_title)

    def _build_musical_work_id(self, musical_work):
        if self._track.iswc:
            musical_work_id = self._build_sub_element(musical_work, "MusicalWorkId")
            self._build_sub_element(musical_work_id, "ISWC", self._track.iswc)

    def _build_contributors(self, contributors, role, work, index):
        for name in contributors:
            contributor = self._build_sub_element(work, "MusicalWorkContributorReference", Sequence=str(index))
            self._build_sub_element(contributor, "MusicalWorkContributorReference", self._parties.reference_for(name))
            self._build_sub_element(contributor, "MusicalWorkContributorRole", role)
            index += 1

        return index


class MusicalWorkList(Section):
    def __init__(self, works):
        self._works = works

    def reference_for(self, name):
        return self._works[name].reference if name in self._works else None

    def write_to(self, root):
        musical_works = self._build_sub_element(root, "MusicalWorkList")
        for work in self._works.values():
            work.write_to(musical_works)

    @classmethod
    def from_(cls, project, parties):
        return cls({track.track_title: MusicalWork(idx, track, parties) for idx, track in enumerate(project.tracks)})
