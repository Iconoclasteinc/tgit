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


class SoundRecording(Section):
    """
    Supported :
        ResourceReference, MusicalWorkSoundRecording, MainArtist, SupplementalArtist, SoundRecordingId/ISRC, Duration,
        Title/TitleText, SoundRecordingMusicalWorkReference,
        SoundRecordingContributorReference/SoundRecordingContributorReference

    Not Supported :
        Version, LanguageOfPerformance, SequenceNumber, KeySignature, TimeSignature, Tempo, Comment,
        SoundRecordingContributorReference/SoundRecordingContributorRelationshipType (not found in avs NS),
        SoundRecordingContributorReference/SoundRecordingContributorRole (not found in avs NS),
        SoundRecordingContributorReference/SoundRecordingContributorInstrument (not found in avs NS),
        SoundRecordingSessionReference, SoundRecordingRecordingComponentReference
    """

    def __init__(self, sequence, track, parties, works):
        self._sequence = sequence
        self._works = works
        self._parties = parties
        self._track = track

    @property
    def reference(self):
        return "A-{0:05d}".format(self._sequence)

    def write_to(self, root):
        sound_recording = self._build_sub_element(root, "SoundRecording")
        self._build_sub_element(sound_recording, "ResourceReference", self.reference)
        self._build_sub_element(sound_recording, "Duration", self._to_iso_8601_duration(self._track.duration))
        self._build_sub_element(sound_recording, "SoundRecordingType", "MusicalWorkSoundRecording")
        self._build_main_artist(sound_recording)
        self._build_supplemental_artist(sound_recording)
        self._build_sound_recording_id(sound_recording)
        self._build_title(sound_recording)
        self._build_musical_work_reference(sound_recording)
        self._build_contributors(sound_recording)

    def _build_contributors(self, sound_recording):
        contributor = self._build_sub_element(sound_recording, "SoundRecordingContributorReference")
        for _, musician in self._track.album.guest_performers:
            self._build_sub_element(contributor, "SoundRecordingContributorReference",
                                    self._parties.reference_for(musician))
        if self._track.recording_studio:
            self._build_sub_element(contributor, "SoundRecordingContributorReference",
                                    self._parties.reference_for(self._track.recording_studio))
        if self._track.production_company:
            self._build_sub_element(contributor, "SoundRecordingContributorReference",
                                    self._parties.reference_for(self._track.production_company))
        if self._track.music_producer:
            self._build_sub_element(contributor, "SoundRecordingContributorReference",
                                    self._parties.reference_for(self._track.music_producer))
        if self._track.mixer:
            self._build_sub_element(contributor, "SoundRecordingContributorReference",
                                    self._parties.reference_for(self._track.mixer))

    def _build_musical_work_reference(self, sound_recording):
        if self._track.track_title:
            self._build_sub_element(sound_recording, "SoundRecordingMusicalWorkReference",
                                    self._works.reference_for(self._track.track_title))

    def _build_sound_recording_id(self, sound_recording):
        if self._track.isrc:
            sound_recording_id = self._build_sub_element(sound_recording, "SoundRecordingId")
            self._build_sub_element(sound_recording_id, "ISRC", self._track.isrc)

    def _build_supplemental_artist(self, sound_recording):
        if self._track.featured_guest:
            self._build_sub_element(sound_recording, "SupplementalArtist", self._parties.reference_for(
                self._track.featured_guest))

    def _build_main_artist(self, sound_recording):
        main_artist = self._track.lead_performer if self._track.album.compilation else self._track.album.lead_performer
        if main_artist:
            self._build_sub_element(sound_recording, "MainArtist", self._parties.reference_for(main_artist))

    def _build_title(self, recording):
        if self._track.track_title:
            title = self._build_sub_element(recording, "Title", TitleType="OriginalTitle")
            self._build_sub_element(title, "TitleText", self._track.track_title)

    @staticmethod
    def _to_iso_8601_duration(duration_in_seconds):
        if not duration_in_seconds:
            return ""

        minutes, seconds = divmod(round(duration_in_seconds), 60)

        return "PT{}M{}S".format(minutes, seconds)


class ResourceList(Section):
    def __init__(self, resources):
        self._resources = resources

    def write_to(self, root):
        resources = self._build_sub_element(root, "ResourceList")
        for resource in self._resources:
            resource.write_to(resources)

    @classmethod
    def from_(cls, project, parties, works):
        return cls([SoundRecording(index, track, parties, works) for index, track in enumerate(project.tracks)])
