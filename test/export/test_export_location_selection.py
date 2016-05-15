# -*- coding: utf-8 -*-
import pytest
from flexmock import flexmock
from hamcrest import assert_that, equal_to, has_items

from test import exception_with_message
from testing.builders import make_album
from tgit.export.exporter import ExportLocationSelection
from tgit.user_preferences import UserPreferences

pytestmark = pytest.mark.unit


def make_export_location_selection(project=make_album(), preferences=UserPreferences()):
    return ExportLocationSelection(project, preferences)


def test_defaults_in_user_preference_directory():
    prefs = UserPreferences()
    prefs.export_location = "directory"

    assert_that(make_export_location_selection(preferences=prefs).directory, equal_to("directory"),
                "The default directory.")


def test_supports_xml_format():
    assert_that(make_export_location_selection().extensions, has_items("xml"), "XML extension supported.")


def test_updates_directory_on_navigation():
    selection = make_export_location_selection()
    selection.directory_changed("new directory")

    assert_that(selection.directory, equal_to("new directory"), "The current directory.")


def test_uses_project_name_as_default_file_name():
    selection = make_export_location_selection(make_album(release_name="Honeycomb"))

    assert_that(selection.default_file_name, equal_to("Honeycomb.xml"), "The default file name.")


def test_reports_failure():
    listener = flexmock()
    listener.should_receive("failed").with_args(exception_with_message("failed")).once()

    selection = make_export_location_selection()
    selection.on_failure.subscribe(listener.failed)

    selection.failed(Exception("failed"))
