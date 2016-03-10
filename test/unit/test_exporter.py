from hamcrest import assert_that, equal_to, same_instance, is_, has_item, contains_string
import pytest

from test.util.builders import make_album, make_track
from test.util.doubles import FakeWorkbook, FakeFormat
from test.util.workspace import AlbumWorkspace
from tgit import export
from tgit.export import exporter

pytestmark = pytest.mark.unit


@pytest.yield_fixture
def workspace(tmpdir):
    album_workspace = AlbumWorkspace(tmpdir.mkdir("workspace"))
    yield album_workspace
    album_workspace.delete()


def test_exports_as_soproq():
    confirmation_message_seen = False

    def load_workbook():
        return workbook

    def confirm():
        nonlocal confirmation_message_seen
        confirmation_message_seen = True

    workbook = FakeWorkbook()
    formatter = FakeFormat()
    exporter.as_soproq_using(load_workbook, confirm, formatter)("an album", "/path/to/save/file")

    assert_that(formatter.album, equal_to("an album"), "the album")
    assert_that(formatter.workbook, same_instance(workbook), "the workbook")
    assert_that(workbook.filename, equal_to("/path/to/save/file"), "the file path")
    assert_that(confirmation_message_seen, is_(True), "the default values message")


def test_exports_album_as_csv_encoded_file(workspace):
    album = make_album(tracks=[make_track(track_title="Les Comédiens")])
    destination_file = workspace.file("french.csv")

    export.as_csv(album, destination_file)

    def read_lines(file):
        content = open(file, "r", encoding="windows-1252").read()
        return content.split("\n")

    assert_that(read_lines(destination_file), has_item(contains_string("Les Comédiens")))
