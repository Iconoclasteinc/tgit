# -*- coding: utf-8 -*-

from xml.etree.ElementTree import Element

import pytest
from hamcrest import assert_that, none, equal_to

from testing.builders import make_album, make_track
from tgit.export.rin_format_models import Party, PartyList


@pytest.fixture
def root():
    return Element("root")


def test_writes_main_artist_as_party(root):
    project = make_album(lead_performer="Joel Miller")
    PartyList.from_(project).write_to(root)

    assert_full_name(root, equal_to("Joel Miller"), "The main artist full name")
    assert_is_organization(root, equal_to("false"), "The main artist is an organization")


def test_writes_party_id(root):
    project = make_album(lead_performer="Joel Miller", isnis={"Joel Miller": "0000000123456789"})
    PartyList.from_(project).write_to(root)

    assert_party_id(root, equal_to("0000000123456789"), "The main artist ISNI")


def test_ommits_party_id_when_no_isni_is_given(root):
    party = Party("...")
    party.write_to(root)
    assert_that(root.find("./Party/PartyId"), none(), "The party ID")


def test_writes_record_label_as_party(root):
    project = make_album(label_name="Effendi Records inc.")
    PartyList.from_(project).write_to(root)

    assert_full_name(root, equal_to("Effendi Records inc."), "The record label name")
    assert_is_organization(root, equal_to("true"), "The record label is an organization")


def test_writes_musicians_as_party(root):
    project = make_album(guest_performers=[("...", "Joel Miller")])
    PartyList.from_(project).write_to(root)

    assert_full_name(root, equal_to("Joel Miller"), "The musician full name")
    assert_is_organization(root, equal_to("false"), "The musician is an organization")


def test_writes_track_main_artist_as_party(root):
    project = make_album(compilation=True, tracks=[make_track(lead_performer="Joel Miller")])
    PartyList.from_(project).write_to(root)

    assert_full_name(root, equal_to("Joel Miller"), "The track's main artist name")
    assert_is_organization(root, equal_to("false"), "The track's main artist is an organization")


def test_writes_track_featured_guest_as_party(root):
    project = make_album(tracks=[make_track(featured_guest="Joel Miller")])
    PartyList.from_(project).write_to(root)

    assert_full_name(root, equal_to("Joel Miller"), "The track's featured guest name")
    assert_is_organization(root, equal_to("false"), "The track's featured guest is an organization")


def test_writes_track_lyricists_as_party(root):
    project = make_album(tracks=[make_track(lyricist=["Joel Miller"])])
    PartyList.from_(project).write_to(root)

    assert_full_name(root, equal_to("Joel Miller"), "The track's lyricists name")
    assert_is_organization(root, equal_to("false"), "The track's lyricists is an organization")


def test_writes_track_composers_as_party(root):
    project = make_album(tracks=[make_track(composer=["Joel Miller"])])
    PartyList.from_(project).write_to(root)

    assert_full_name(root, equal_to("Joel Miller"), "The track's composers name")
    assert_is_organization(root, equal_to("false"), "The track's composers is an organization")


def test_writes_track_publishers_as_party(root):
    project = make_album(tracks=[make_track(publisher=["Effendi Records inc."])])
    PartyList.from_(project).write_to(root)

    assert_full_name(root, equal_to("Effendi Records inc."), "The track's publishers name")
    assert_is_organization(root, equal_to("true"), "The track's publishers is an organization")


def test_writes_track_recording_studio_as_party(root):
    project = make_album(tracks=[make_track(recording_studio="Effendi Records inc.")])
    PartyList.from_(project).write_to(root)

    assert_full_name(root, equal_to("Effendi Records inc."), "The track's recording studio name")
    assert_is_organization(root, equal_to("true"), "The track's recording studio is an organization")


def test_writes_track_production_company_as_party(root):
    project = make_album(tracks=[make_track(production_company="Effendi Records inc.")])
    PartyList.from_(project).write_to(root)

    assert_full_name(root, equal_to("Effendi Records inc."), "The track's production company name")
    assert_is_organization(root, equal_to("true"), "The track's production company is an organization")


def test_writes_track_music_producer_as_party(root):
    project = make_album(tracks=[make_track(music_producer="Joel Miller")])
    PartyList.from_(project).write_to(root)

    assert_full_name(root, equal_to("Joel Miller"), "The track's music producer name")
    assert_is_organization(root, equal_to("false"), "The track's music producer is an organization")


def test_writes_track_mixer_as_party(root):
    project = make_album(tracks=[make_track(mixer="Joel Miller")])
    PartyList.from_(project).write_to(root)

    assert_full_name(root, equal_to("Joel Miller"), "The track's mixer name")
    assert_is_organization(root, equal_to("false"), "The track's mixer is an organization")


def test_adds_party_only_once(root):
    project = make_album(lead_performer="Joel Miller",
                         guest_performers=[("...", "Joel Miller")],
                         isnis={"Joel Miller": "0000000123456789"})

    PartyList.from_(project).write_to(root)

    parties = root.findall("./PartyList/Party")
    assert_that(len(parties), equal_to(1), "The number of parties")


def assert_full_name(element, matching, description):
    full_name = element.findtext("./PartyList/Party/PartyName/FullName")
    assert_that(full_name, matching, description)


def assert_is_organization(element, matching, description):
    is_organization = element.findtext("./PartyList/Party/IsOrganization")
    assert_that(is_organization, matching, description)


def assert_party_id(element, matching, description):
    party_id = element.find("./PartyList/Party/PartyId")
    assert_that(party_id.attrib["IsISNI"], equal_to("true"), "The party ID is an ISNI")
    assert_that(party_id.findtext("./ISNI"), matching, description)
