from datetime import date

from hamcrest import assert_that, equal_to

from openpyxl import Workbook

from test.util import builders as build
from tgit.export.soproq_format import write


def test_writes_tracks_to_workbook():
    album = build.album(
        release_name="Release Name",
        lead_performer="Lead Performer",
        isni="0000123456789",
        compilation=True,
        guest_performers=[("Instrument1", "Performer1"), ("Instrument2", "Performer2")],
        label_name="Label Name",
        catalog_number="Catalog Number",
        upc="Barcode",
        comments="Comments\n...\n...",
        release_time="2014-05-10",
        recording_time="2013-05-10",
        recording_studios="Studios",
        producer="Artistic Producer",
        mixer="Mixing Engineer",
        primary_style="Genre")

    album.add_track(build.track(
        track_title="Track Title",
        versionInfo="Version Info",
        featuredGuest="Featuring",
        lyrics="Lyrics\n...\...\n...",
        language="eng",
        publisher="Publisher",
        lyricist="Lyricist",
        composer="Composer",
        isrc="ISRC",
        labels="Tag1 Tag2 Tag3",
        duration=60))

    album.addTrack(build.track(
        track_title="Track Title1",
        versionInfo="Version Info1",
        featuredGuest="Featuring1",
        lyrics="Lyrics\n...\...\n...1",
        language="eng1",
        publisher="Publisher1",
        lyricist="Lyricist1",
        composer="Composer1",
        isrc="ISRC1",
        labels="Tag1 Tag2 Tag31",
        duration=120))

    workbook = Workbook()

    write(album, workbook)

    has_rights_holder(workbook.active, "Label Name", str(date.today()))
    has_line_metadata(workbook.active,
                      A13="Release Name",
                      B13="Lead Performer",
                      C13="",
                      D13="Label Name",
                      E13="Label Name",
                      F13="",
                      G13="Catalog Number",
                      H13="Barcode",
                      I13="2014-05-10",
                      J13="",
                      K13="O",
                      L13="1",
                      M13="Track Title",
                      N13="Lead Performer",
                      O13="",
                      P13="ISRC",
                      Q13="00:01:00",
                      R13="",
                      S13="2013",
                      T13="Artistic Producer",
                      U13="",
                      V13="",
                      W13="",
                      X13="",
                      Y13="",
                      Z13="",
                      AA13="")

    has_line_metadata(workbook.active,
                      A14="Release Name",
                      B14="Lead Performer",
                      C14="",
                      D14="Label Name",
                      E14="Label Name",
                      F14="",
                      G14="Catalog Number",
                      H14="Barcode",
                      I14="2014-05-10",
                      J14="",
                      K14="O",
                      L14="2",
                      M14="Track Title1",
                      N14="Lead Performer",
                      O14="",
                      P14="ISRC1",
                      Q14="00:02:00",
                      R14="",
                      S14="2013",
                      T14="Artistic Producer",
                      U14="",
                      V14="",
                      W14="",
                      X14="",
                      Y14="",
                      Z14="",
                      AA14="")


def has_rights_holder(worksheet, name, datetime):
    assert_that(worksheet["B6"].value, equal_to(name), "Rights holder name")
    assert_that(worksheet["C6"].value, equal_to(datetime), "Declaration date")


def has_line_metadata(worksheet, **cells):
    for key, value in cells.items():
        assert_that(worksheet[key].value, equal_to(cells[key]), key)
