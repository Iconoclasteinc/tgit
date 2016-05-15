from xml.etree.ElementTree import ElementTree

from flexmock import flexmock
import pytest
from hamcrest import assert_that, equal_to, same_instance, is_, has_item, contains_string, match_equality, instance_of

from cute import platforms
from testing.builders import make_album, make_track
from testing.doubles import FakeWorkbook, FakeFormat
from testing.workspace import AlbumWorkspace
from tgit import export
from tgit.export import exporter

pytestmark = pytest.mark.unit


@pytest.yield_fixture
def workspace(tmpdir):
    project_workspace = AlbumWorkspace(tmpdir.mkdir("workspace"))
    yield project_workspace
    project_workspace.delete()


@pytest.fixture
def export_location_selection():
    return flexmock()


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


def test_exports_project_as_csv_encoded_file(workspace):
    project = make_album(tracks=[make_track(track_title="Les Comédiens")])
    destination_file = workspace.file("french.csv")

    export.as_csv(project, destination_file)

    def read_lines(file):
        content = open(file, "r", encoding="windows-1252").read()
        return content.split("\n")

    assert_that(read_lines(destination_file), has_item(contains_string("Les Comédiens")))


def test_exports_project_as_ddex_rin_xml_file(workspace, export_location_selection):
    project = make_album(lead_performer="Joel Miller", tracks=[make_track(track_title="Chevere!")])
    destination_file = workspace.file("Honeycomb.xml")

    export.as_ddex_rin(project, export_location_selection)(destination_file)

    root = ElementTree().parse(destination_file)
    assert_that(root.tag, contains_string("RecordingInformationNotification"), "The outer tag")


def test_reports_failure_on_export_error(export_location_selection):
    project = make_album(lead_performer="Joel Miller", tracks=[make_track(track_title="Chevere!")])
    destination_file = "C:" if platforms.windows else "/"

    export_location_selection.should_receive("failed").with_args(match_equality(instance_of(PermissionError))).once()

    export.as_ddex_rin(project, export_location_selection)(destination_file)
