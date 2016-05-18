# -*- coding: utf-8 -*-
import os
from xml.etree import ElementTree

from hamcrest import assert_that, equal_to, contains_string, not_none
import pytest

from testing.builders import make_album, make_track
from tgit.export.ddex import rin

pytestmark = pytest.mark.unit


@pytest.fixture
def filename(tmpdir):
    return os.path.join(tmpdir.strpath, "Honeycomb.xml")


def test_writes_xml_enveloppe(filename):
    project = make_album()
    root = rin.write(project, filename)

    xml = ElementTree.tostring(root, encoding="unicode")
    assert_that(xml, contains_string("xmlns:rin=\"http://ddex.net/xml/rin/10\""), "The RIN namespace declaration")
    assert_that(xml, contains_string("xmlns:avs=\"http://ddex.net/xml/avs/avs\""), "The AVS namespace declaration")
    assert_that(xml, contains_string("xmlns:ds=\"http://www.w3.org/2000/09/xmldsig#\""), "The DS namespace declaration")
    assert_that(xml, contains_string("xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\""),
                "The XSI namespace declaration")

    assert_that(root.tag, equal_to("rin:RecordingInformationNotification"), "The outer tag")
    assert_that(root.attrib["xsi:schemaLocation"],
                equal_to("http://ddex.net/xml/rin/10 file:recording-information-notification.xsd"),
                "The schema location")
    assert_that(root.attrib["SchemaVersionId"], equal_to("rin/10"), "The schema version id")
    assert_that(root.attrib["LanguageAndScriptCode"], equal_to("en"), "The language code")


def test_writes_party_list(filename):
    project = make_album(lead_performer="Joel Miller")
    root = rin.write(project, filename)

    party_list = root.find("./PartyList")
    assert_that(party_list, not_none(), "The party list")

    party = party_list.find("./Party")
    assert_that(party, not_none(), "The party")


def test_writes_file_header(filename):
    project = make_album()
    root = rin.write(project, filename)

    file_header = root.find("./FileHeader")
    assert_that(file_header, not_none(), "The file header")


def test_writes_musical_work_list(filename):
    project = make_album(tracks=[make_track(track_title="Chevere!"), make_track(track_title="Zumbar")])
    root = rin.write(project, filename)

    musical_work_list = root.find("./MusicalWorkList")
    assert_that(musical_work_list, not_none(), "The musical work list")

    musical_works = musical_work_list.findall("./MusicalWork")
    assert_that(len(musical_works), equal_to(2), "The musical work")


def test_writes_resources_list(filename):
    project = make_album(tracks=[make_track(track_title="Chevere!"), make_track(track_title="Zumbar")])
    root = rin.write(project, filename)

    resource_list = root.find("./ResourceList")
    assert_that(resource_list, not_none(), "The resource list")

    recordings = resource_list.findall("./SoundRecording")
    assert_that(len(recordings), equal_to(2), "The recordings")