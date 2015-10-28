from hamcrest import assert_that, equal_to, same_instance
from test.util.doubles import FakeWorkbook, FakeFormat

from tgit.export import exporter


def test_exports_as_soproq():
    def load_workbook():
        return workbook

    workbook = FakeWorkbook()
    formatter = FakeFormat()
    exporter.as_soproq_using(load_workbook, formatter)("an album", "/path/to/save/file")

    assert_that(formatter.album, equal_to("an album"), "the album")
    assert_that(formatter.workbook, same_instance(workbook), "the workbook")
    assert_that(workbook.filename, equal_to("/path/to/save/file"), "the file path")
