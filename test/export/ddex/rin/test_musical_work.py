# -*- coding: utf-8 -*-

from flexmock import flexmock
import pytest
from hamcrest import assert_that, none, equal_to, starts_with, ends_with

from testing.builders import make_track
from tgit.export.ddex.rin.musical_work import MusicalWork, MusicalWorkList

pytestmark = pytest.mark.unit


@pytest.fixture
def party_list():
    return flexmock()


def test_writes_the_musical_work_reference(root, party_list):
    track = make_track()

    MusicalWork(13, track, party_list).write_to(root)

    reference = root.findtext("./MusicalWork/MusicalWorkReference")
    assert_that(reference, starts_with("W"), "The musical work reference")
    assert_that(reference, ends_with("13"), "The musical work reference")


def test_writes_iswc(root, party_list):
    track = make_track(iswc="0000000123456789")
    MusicalWork(0, track, party_list).write_to(root)
    assert_that(root.findtext("./MusicalWork/MusicalWorkId/ISWC"), equal_to("0000000123456789"), "The ISWC")


def test_omits_iswc_when_not_entered(root, party_list):
    track = make_track()
    MusicalWork(0, track, party_list).write_to(root)
    assert_that(root.find("./MusicalWork/MusicalWorkId"), none(), "The ISWC")


def test_writes_lyrics(root, party_list):
    track = make_track(lyrics="lyrics...")
    MusicalWork(0, track, party_list).write_to(root)
    assert_that(root.findtext("./MusicalWork/Lyrics"), equal_to("lyrics..."), "The lyrics")


def test_omits_lyrics_when_not_entered(root, party_list):
    track = make_track()
    MusicalWork(0, track, party_list).write_to(root)
    assert_that(root.find("./MusicalWork/Lyrics"), none(), "The lyrics")


def test_writes_title(root, party_list):
    track = make_track(track_title="Chevere!")
    MusicalWork(0, track, party_list).write_to(root)
    assert_that(root.find("./MusicalWork/Title").attrib["TitleType"], equal_to("OriginalTitle"), "The track title type")
    assert_that(root.findtext("./MusicalWork/Title/TitleText"), equal_to("Chevere!"), "The track title")


def test_omits_title_when_not_entered(root, party_list):
    track = make_track()
    MusicalWork(0, track, party_list).write_to(root)
    assert_that(root.find("./MusicalWork/Title"), none(), "The track title")


def test_writes_comments(root, party_list):
    track = make_track(comments="comments...")
    MusicalWork(0, track, party_list).write_to(root)
    assert_that(root.findtext("./MusicalWork/Comment"), equal_to("comments..."), "The track comments")


def test_omits_comments_when_not_entered(root, party_list):
    track = make_track()
    MusicalWork(0, track, party_list).write_to(root)
    assert_that(root.find("./MusicalWork/Comment"), none(), "The track comments")


def test_writes_lyricist(root, party_list):
    party_list.should_receive("reference_for").with_args("Joel Miller").and_return("P-00001").once()
    track = make_track(lyricist=["Joel Miller"])
    MusicalWork(0, track, party_list).write_to(root)
    assert_that(root.findtext("./MusicalWork/MusicalWorkContributorReference/MusicalWorkContributorRole"),
                equal_to("Lyricist"), "The track lyricists")
    assert_that(root.findtext("./MusicalWork/MusicalWorkContributorReference/MusicalWorkContributorReference"),
                equal_to("P-00001"), "The party reference")


def test_omits_lyricist_when_not_entered(root, party_list):
    track = make_track()
    MusicalWork(0, track, party_list).write_to(root)
    assert_that(root.find("./MusicalWork/MusicalWorkContributorReference"), none(),
                "The track lyricists")


def test_writes_composer(root, party_list):
    party_list.should_receive("reference_for").with_args("Joel Miller").and_return("P-00001").once()
    track = make_track(composer=["Joel Miller"])
    MusicalWork(0, track, party_list).write_to(root)
    assert_that(root.findtext("./MusicalWork/MusicalWorkContributorReference/MusicalWorkContributorRole"),
                equal_to("Composer"), "The track composers")
    assert_that(root.findtext("./MusicalWork/MusicalWorkContributorReference/MusicalWorkContributorReference"),
                equal_to("P-00001"), "The party reference")


def test_omits_composer_when_not_entered(root, party_list):
    track = make_track()
    MusicalWork(0, track, party_list).write_to(root)
    assert_that(root.find("./MusicalWork/MusicalWorkContributorReference"), none(),
                "The track composers")


def test_writes_composer_lyricists_when_existing_in_both_lists(root, party_list):
    party_list.should_receive("reference_for").with_args("Joel Miller").and_return("P-00001").once()
    track = make_track(composer=["Joel Miller"], lyricist=["Joel Miller"])
    MusicalWork(0, track, party_list).write_to(root)

    assert_that(len(root.findall("./MusicalWork/MusicalWorkContributorReference")), equal_to(1),
                "The track composers/lyricists")
    assert_that(root.findtext("./MusicalWork/MusicalWorkContributorReference/MusicalWorkContributorRole"),
                equal_to("ComposerLyricist"), "The track composers/lyricists")
    assert_that(root.findtext("./MusicalWork/MusicalWorkContributorReference/MusicalWorkContributorReference"),
                equal_to("P-00001"), "The party reference")


def test_writes_publishers(root, party_list):
    party_list.should_receive("reference_for").with_args("Effendi Records inc.").and_return("P-00001").once()
    track = make_track(publisher=["Effendi Records inc."])
    MusicalWork(0, track, party_list).write_to(root)
    assert_that(root.findtext("./MusicalWork/MusicalWorkContributorReference/MusicalWorkContributorRole"),
                equal_to("OriginalPublisher"), "The track publishers")
    assert_that(root.findtext("./MusicalWork/MusicalWorkContributorReference/MusicalWorkContributorReference"),
                equal_to("P-00001"), "The party reference")


def test_omits_publishers_when_not_entered(root, party_list):
    track = make_track()
    MusicalWork(0, track, party_list).write_to(root)
    assert_that(root.find("./MusicalWork/MusicalWorkContributorReference"), none(), "The track publishers")


def test_writes_contributor_reference_sequence(root, party_list):
    party_list.should_receive("reference_for")
    track = make_track(composer=["Joel Miller"], lyricist=["John Roney"], publisher=["Effendi Records inc."])
    MusicalWork(0, track, party_list).write_to(root)

    contributors = root.findall("./MusicalWork/MusicalWorkContributorReference")
    assert_that(contributors[0].attrib["Sequence"], equal_to("0"), "The contributor sequence")
    assert_that(contributors[1].attrib["Sequence"], equal_to("1"), "The contributor sequence")
    assert_that(contributors[2].attrib["Sequence"], equal_to("2"), "The contributor sequence")


def test_fetch_reference_of_a_party_by_name():
    musical_work = flexmock(reference="P-00001")
    musical_work_list = MusicalWorkList({"Joel Miller": musical_work})

    assert_that(musical_work_list.reference_for("Joel Miller"), equal_to("P-00001"), "The musical work reference")


def test_returns_none_reference_when_a_party_is_not_found():
    musical_work_list = MusicalWorkList({})

    assert_that(musical_work_list.reference_for("Joel Miller"), none(), "The musical work reference")
