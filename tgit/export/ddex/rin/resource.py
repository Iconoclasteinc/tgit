# -*- coding: utf-8 -*-
from xml.etree import ElementTree


class SoundRecording:
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

    def __init__(self, sequence, track, party_list, musical_work_list):
        self._sequence = sequence
        self._musical_work_list = musical_work_list
        self._party_list = party_list
        self._track = track

    @property
    def reference(self):
        return "A-{0:05d}".format(self._sequence)

    def write_to(self, root):
        sound_recording = ElementTree.SubElement(root, "SoundRecording")

        resource_reference = ElementTree.SubElement(sound_recording, "ResourceReference")
        resource_reference.text = self.reference

        duration = ElementTree.SubElement(sound_recording, "Duration")
        duration.text = self._to_iso_8601_duration(self._track.duration)

        sound_recording_type = ElementTree.SubElement(sound_recording, "SoundRecordingType")
        sound_recording_type.text = "MusicalWorkSoundRecording"  # todo validate hypothesis

        main_artist = self._track.lead_performer if self._track.album.compilation else self._track.album.lead_performer
        if main_artist:
            main_artist_reference = ElementTree.SubElement(sound_recording, "MainArtist")
            main_artist_reference.text = self._party_list.reference_for(main_artist)

        if self._track.featured_guest:
            featured_guest_reference = ElementTree.SubElement(sound_recording, "SupplementalArtist")
            featured_guest_reference.text = self._party_list.reference_for(
                self._track.featured_guest)  # todo validate hypothesis

        if self._track.isrc:
            sound_recording_id = ElementTree.SubElement(sound_recording, "SoundRecordingId")
            isrc = ElementTree.SubElement(sound_recording_id, "ISRC")
            isrc.text = self._track.isrc

        if self._track.track_title:
            title = ElementTree.SubElement(sound_recording, "Title")
            title.attrib["TitleType"] = "OriginalTitle"  # todo validate hypothesis
            title_text = ElementTree.SubElement(title, "TitleText")
            title_text.text = self._track.track_title
            musical_work_reference = ElementTree.SubElement(sound_recording, "SoundRecordingMusicalWorkReference")
            musical_work_reference.text = self._musical_work_list.reference_for(self._track.track_title)

        contributor = ElementTree.SubElement(sound_recording, "SoundRecordingContributorReference")
        for _, musician in self._track.album.guest_performers or []:
            contributor_reference = ElementTree.SubElement(contributor, "SoundRecordingContributorReference")
            contributor_reference.text = self._party_list.reference_for(musician)

        if self._track.recording_studio:
            contributor_reference = ElementTree.SubElement(contributor, "SoundRecordingContributorReference")
            contributor_reference.text = self._party_list.reference_for(self._track.recording_studio)

        if self._track.production_company:
            contributor_reference = ElementTree.SubElement(contributor, "SoundRecordingContributorReference")
            contributor_reference.text = self._party_list.reference_for(self._track.production_company)

        if self._track.music_producer:
            contributor_reference = ElementTree.SubElement(contributor, "SoundRecordingContributorReference")
            contributor_reference.text = self._party_list.reference_for(self._track.music_producer)

        if self._track.mixer:
            contributor_reference = ElementTree.SubElement(contributor, "SoundRecordingContributorReference")
            contributor_reference.text = self._party_list.reference_for(self._track.mixer)

    @staticmethod
    def _to_iso_8601_duration(duration_in_seconds):
        if not duration_in_seconds:
            return ""

        minutes, seconds = divmod(round(duration_in_seconds), 60)

        return "PT{}M{}S".format(minutes, seconds)


class ResourceList:
    def __init__(self, resources):
        self._resources = resources

    def write_to(self, root):
        resource_list_element = ElementTree.SubElement(root, "ResourceList")
        for resource in self._resources:
            resource.write_to(resource_list_element)

    @classmethod
    def from_(cls, project, party_list, musical_work_list):
        return cls(
            [SoundRecording(index, track, party_list, musical_work_list) for index, track in enumerate(project.tracks)])
