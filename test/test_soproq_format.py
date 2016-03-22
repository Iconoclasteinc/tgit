from datetime import date

import pytest
from hamcrest import assert_that, equal_to
from openpyxl import Workbook

from test.util import builders as build
from tgit.export.soproq_format import write

pytestmark = pytest.mark.unit


def test_writes_tracks_to_workbook():
    album = build.album(
        release_name="Release Name",
        lead_performer="Lead Performer",
        lead_performer_region=("CA",),
        compilation=False,
        label_name="Label Name",
        catalog_number="Catalog Number",
        upc="Barcode",
        release_time="2014-05-10")

    album.add_track(build.track(track_title="Track Title",
                                isrc="ISRC",
                                duration=60,
                                recording_studio_region=("CA",),
                                production_company="Production Company",
                                production_company_region=("US",),
                                recording_time="2013-05-10"))
    album.add_track(build.track(track_title="Track Title1",
                                isrc="ISRC1",
                                duration=120,
                                recording_studio_region=("CA",),
                                production_company="Production Company",
                                production_company_region=("US",),
                                recording_time="2013-05-10"))

    workbook = Workbook()

    write(album, workbook)

    has_rights_holder(workbook.active, "Label Name", str(date.today()))
    has_line_metadata(workbook.active,
                      A13="Release Name",
                      B13="Lead Performer",
                      C13="CAN",
                      D13="Label Name",
                      E13="Label Name",
                      F13="",
                      G13="Catalog Number",
                      H13="Barcode",
                      I13="2014-05-10",
                      J13="",
                      K13="N",
                      L13="1",
                      M13="Track Title",
                      N13="Lead Performer",
                      O13="CAN",
                      P13="ISRC",
                      Q13="00:01:00",
                      R13="CAN",
                      S13="2013",
                      T13="Production Company",
                      U13="USA",
                      V13="RE/CP/Repro",
                      W13="100",
                      X13="WW",
                      Y13="",
                      Z13="",
                      AA13="")

    has_line_metadata(workbook.active,
                      A14="Release Name",
                      B14="Lead Performer",
                      C14="CAN",
                      D14="Label Name",
                      E14="Label Name",
                      F14="",
                      G14="Catalog Number",
                      H14="Barcode",
                      I14="2014-05-10",
                      J14="",
                      K14="N",
                      L14="2",
                      M14="Track Title1",
                      N14="Lead Performer",
                      O14="CAN",
                      P14="ISRC1",
                      Q14="00:02:00",
                      R14="CAN",
                      S14="2013",
                      T14="Production Company",
                      U14="USA",
                      V14="RE/CP/Repro",
                      W14="100",
                      X14="WW",
                      Y14="",
                      Z14="",
                      AA14="")


def test_writes_compilation_tracks_to_workbook():
    album = build.album(
        release_name="Release Name",
        lead_performer="Various Artists",
        compilation=True)

    album.add_track(build.track(lead_performer="performer"))

    workbook = Workbook()

    write(album, workbook)

    has_line_metadata(workbook.active,
                      A13="Release Name",
                      B13="Artistes Variés",
                      N13="performer",
                      K13="O")


def has_rights_holder(worksheet, name, datetime):
    assert_that(worksheet["A6"].value, equal_to(name), "Rights holder name")
    assert_that(worksheet["C6"].value, equal_to(datetime), "Declaration date")


def has_line_metadata(worksheet, **cells):
    for key, value in cells.items():
        assert_that(worksheet[key].value, equal_to(cells[key]), key)
