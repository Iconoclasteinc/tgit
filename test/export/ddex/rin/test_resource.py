# -*- coding: utf-8 -*-
from flexmock import flexmock
from hamcrest import assert_that, starts_with, ends_with, equal_to, none, contains_inanyorder
import pytest

from testing.builders import make_track, make_album
from tgit.export.ddex.rin.resource import SoundRecording

pytestmark = pytest.mark.unit


@pytest.fixture
def party_list():
    list_ = flexmock()
    list_.should_receive("reference_for")
    return list_


@pytest.fixture
def musical_work_list():
    list_ = flexmock()
    list_.should_receive("reference_for")
    return list_


def test_writes_the_resource_reference(root, party_list, musical_work_list):
    track = make_track()
    _ = make_album(tracks=[track])

    SoundRecording(13, track, party_list, musical_work_list).write_to(root)

    reference = root.findtext("./SoundRecording/ResourceReference")
    assert_that(reference, starts_with("A"), "The resource reference")
    assert_that(reference, ends_with("13"), "The resource reference")


def test_writes_the_sound_recording_type(root, party_list, musical_work_list):
    track = make_track()
    _ = make_album(tracks=[track])

    SoundRecording(0, track, party_list, musical_work_list).write_to(root)

    type_ = root.findtext("./SoundRecording/SoundRecordingType")
    assert_that(type_, equal_to("MusicalWorkSoundRecording"), "The sound recording type")


def test_writes_the_project_main_artist_reference(root, party_list, musical_work_list):
    party_list.should_receive("reference_for").with_args("Joel Miller").and_return("P-00000")

    track = make_track()
    _ = make_album(lead_performer="Joel Miller", compilation=False, tracks=[track])

    SoundRecording(0, track, party_list, musical_work_list).write_to(root)

    main_artist = root.findtext("./SoundRecording/MainArtist")
    assert_that(main_artist, equal_to("P-00000"), "The main artist reference")


def test_ommits_the_project_main_artist_reference_when_main_artist_not_entered(root, party_list, musical_work_list):
    track = make_track()
    _ = make_album(compilation=False, tracks=[track])

    SoundRecording(0, track, party_list, musical_work_list).write_to(root)

    assert_that(root.find("./SoundRecording/MainArtist"), none(), "The main artist reference")


def test_writes_the_track_main_artist_reference_when_project_is_a_compilation(root, party_list, musical_work_list):
    party_list.should_receive("reference_for").with_args("Joel Miller").and_return("P-00000")

    track = make_track(lead_performer="Joel Miller")
    _ = make_album(compilation=True, tracks=[track])

    SoundRecording(0, track, party_list, musical_work_list).write_to(root)

    main_artist = root.findtext("./SoundRecording/MainArtist")
    assert_that(main_artist, equal_to("P-00000"), "The main artist reference")


def test_ommits_the_track_main_artist_reference_when_main_artist_not_entered(root, party_list, musical_work_list):
    track = make_track()
    _ = make_album(compilation=True, tracks=[track])

    SoundRecording(0, track, party_list, musical_work_list).write_to(root)

    assert_that(root.find("./SoundRecording/MainArtist"), none(), "The main artist reference")


def test_writes_the_featured_guest(root, party_list, musical_work_list):
    party_list.should_receive("reference_for").with_args("Joel Miller").and_return("P-00000")

    track = make_track(featured_guest="Joel Miller")
    _ = make_album(tracks=[track])

    SoundRecording(0, track, party_list, musical_work_list).write_to(root)

    featured_guest = root.findtext("./SoundRecording/SupplementalArtist")
    assert_that(featured_guest, equal_to("P-00000"), "The featured guest reference")


def test_ommits_the_featured_guest_reference_when_not_entered(root, party_list, musical_work_list):
    track = make_track()
    _ = make_album(tracks=[track])

    SoundRecording(0, track, party_list, musical_work_list).write_to(root)

    assert_that(root.find("./SoundRecording/SupplementalArtist"), none(), "The featured guest reference")


def test_writes_the_isrc(root, party_list, musical_work_list):
    track = make_track(isrc="0000000123456789")
    _ = make_album(tracks=[track])

    SoundRecording(0, track, party_list, musical_work_list).write_to(root)

    isrc = root.findtext("./SoundRecording/SoundRecordingId/ISRC")
    assert_that(isrc, equal_to("0000000123456789"), "The isrc")


def test_ommits_the_isrc_when_not_entered(root, party_list, musical_work_list):
    track = make_track()
    _ = make_album(tracks=[track])

    SoundRecording(0, track, party_list, musical_work_list).write_to(root)

    assert_that(root.find("./SoundRecording/SoundRecordingId"), none(), "The isrc")


def test_writes_the_title(root, party_list, musical_work_list):
    track = make_track(track_title="Chevere!")
    _ = make_album(tracks=[track])

    SoundRecording(0, track, party_list, musical_work_list).write_to(root)

    title = root.find("./SoundRecording/Title")
    title_text = title.findtext("./TitleText")
    assert_that(title_text, equal_to("Chevere!"), "The title")
    assert_that(title.attrib["TitleType"], equal_to("OriginalTitle"), "The title type")


def test_ommits_the_title_when_not_entered(root, party_list, musical_work_list):
    track = make_track()
    _ = make_album(tracks=[track])

    SoundRecording(0, track, party_list, musical_work_list).write_to(root)

    assert_that(root.find("./SoundRecording/Title"), none(), "The title")


def test_writes_the_musical_work_reference(root, party_list, musical_work_list):
    musical_work_list.should_receive("reference_for").with_args("Chevere!").and_return("W-00000")

    track = make_track(track_title="Chevere!")
    _ = make_album(tracks=[track])

    SoundRecording(0, track, party_list, musical_work_list).write_to(root)

    musical_work_reference = root.findtext("./SoundRecording/SoundRecordingMusicalWorkReference")
    assert_that(musical_work_reference, equal_to("W-00000"), "The musical work reference")


def test_writes_the_musicians_as_contributor_reference(root, party_list, musical_work_list):
    party_list.should_receive("reference_for").with_args("Joel Miller").and_return("P-00000")
    party_list.should_receive("reference_for").with_args("John Roney").and_return("P-00001")

    track = make_track()
    _ = make_album(guest_performers=[("...", "Joel Miller"), ("...", "John Roney")], tracks=[track])

    SoundRecording(0, track, party_list, musical_work_list).write_to(root)

    contributors = root.findall(
        "./SoundRecording/SoundRecordingContributorReference/SoundRecordingContributorReference")
    contributor_references = [contributor.text for contributor in contributors]

    assert_that(contributor_references, contains_inanyorder("P-00000", "P-00001"), "The musician references")


def test_writes_the_recording_studio_as_contributor_reference(root, party_list, musical_work_list):
    party_list.should_receive("reference_for").with_args("Effendi Records inc.").and_return("P-00000")

    track = make_track(recording_studio="Effendi Records inc.")
    _ = make_album(tracks=[track])

    SoundRecording(0, track, party_list, musical_work_list).write_to(root)

    contributor = root.findtext(
        "./SoundRecording/SoundRecordingContributorReference/SoundRecordingContributorReference")
    assert_that(contributor, equal_to("P-00000"), "The recording studio reference")


def test_writes_the_production_company_as_contributor_reference(root, party_list, musical_work_list):
    party_list.should_receive("reference_for").with_args("Effendi Records inc.").and_return("P-00000")

    track = make_track(production_company="Effendi Records inc.")
    _ = make_album(tracks=[track])

    SoundRecording(0, track, party_list, musical_work_list).write_to(root)

    contributor = root.findtext(
        "./SoundRecording/SoundRecordingContributorReference/SoundRecordingContributorReference")
    assert_that(contributor, equal_to("P-00000"), "The production company reference")


def test_writes_the_music_producer_as_contributor_reference(root, party_list, musical_work_list):
    party_list.should_receive("reference_for").with_args("Effendi Records inc.").and_return("P-00000")

    track = make_track(music_producer="Effendi Records inc.")
    _ = make_album(tracks=[track])

    SoundRecording(0, track, party_list, musical_work_list).write_to(root)

    contributor = root.findtext(
        "./SoundRecording/SoundRecordingContributorReference/SoundRecordingContributorReference")
    assert_that(contributor, equal_to("P-00000"), "The music producer reference")


def test_writes_the_mixer_as_contributor_reference(root, party_list, musical_work_list):
    party_list.should_receive("reference_for").with_args("Effendi Records inc.").and_return("P-00000")

    track = make_track(mixer="Effendi Records inc.")
    _ = make_album(tracks=[track])

    SoundRecording(0, track, party_list, musical_work_list).write_to(root)

    contributor = root.findtext(
        "./SoundRecording/SoundRecordingContributorReference/SoundRecordingContributorReference")
    assert_that(contributor, equal_to("P-00000"), "The mixer reference")


def test_writes_the_duration(root, party_list, musical_work_list):
    track = make_track(duration=125)
    _ = make_album(tracks=[track])

    SoundRecording(0, track, party_list, musical_work_list).write_to(root)

    assert_that(root.findtext("./SoundRecording/Duration"), equal_to("PT2M5S"), "The track duration")
