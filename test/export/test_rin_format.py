# -*- coding: utf-8 -*-
from xml.etree import ElementTree

from hamcrest import assert_that, equal_to, contains_string, not_none
import pytest

from testing.builders import make_album
from tgit.export.rin_format import RinFormat

pytestmark = pytest.mark.unit


@pytest.fixture
def formatter():
    return RinFormat()


def test_writes_xml_enveloppe(formatter):
    project = make_album()
    root = formatter.to_xml(project)

    rin = ElementTree.tostring(root, encoding="unicode")
    assert_that(rin, contains_string("xmlns:rin=\"http://ddex.net/xml/rin/10\""), "The RIN namespace declaration")
    assert_that(rin, contains_string("xmlns:avs=\"http://ddex.net/xml/avs/avs\""), "The AVS namespace declaration")
    assert_that(rin, contains_string("xmlns:ds=\"http://www.w3.org/2000/09/xmldsig#\""), "The DS namespace declaration")
    assert_that(rin, contains_string("xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\""),
                "The XSI namespace declaration")

    assert_that(root.tag, equal_to("rin:RecordingInformationNotification"), "The outer tag")
    assert_that(root.attrib["xsi:schemaLocation"],
                equal_to("http://ddex.net/xml/rin/10 file:recording-information-notification.xsd"),
                "The schema location")
    assert_that(root.attrib["SchemaVersionId"], equal_to("rin/10"), "The schema version id")
    assert_that(root.attrib["LanguageAndScriptCode"], equal_to("en"), "The language code")


def test_writes_party_list(formatter):
    project = make_album(lead_performer="Joel Miller")
    root = formatter.to_xml(project)

    party_list = root.find("./PartyList")
    assert_that(party_list, not_none(), "The party list")

    party = party_list.find("./Party")
    assert_that(party, not_none(), "The party")
