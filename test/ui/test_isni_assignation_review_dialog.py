# -*- coding: utf-8 -*-
import pytest

from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.ui import ignore, show_, close_
from test.util.builders import make_album, make_track
from testing.drivers import IsniAssignationReviewDialogDriver
from tgit.identity import IdentitySelection
from tgit.ui import make_isni_assignation_review_dialog
from tgit.ui.dialogs.isni_assignation_review_dialog import ISNIAssignationReviewDialog

pytestmark = pytest.mark.ui


def show_dialog(isni_selection=IdentitySelection(make_album(), ""), on_assign=ignore):
    dialog = make_isni_assignation_review_dialog(isni_selection, on_assign, delete_on_close=False)
    show_(dialog)
    return dialog


@pytest.yield_fixture()
def driver(prober, automaton):
    dialog_driver = IsniAssignationReviewDialogDriver(window(ISNIAssignationReviewDialog), prober, automaton)
    yield dialog_driver
    close_(dialog_driver)


def test_displays_works(driver):
    selection = IdentitySelection(
        make_album(tracks=[make_track(track_title="Chevere!"), make_track(track_title="Zumbar")]), "")
    _ = show_dialog(selection)
    driver.has_works("Chevere!", "Zumbar")


def test_displays_name(driver):
    selection = IdentitySelection(make_album(), "Joel Miller")
    _ = show_dialog(selection)
    driver.has_name("Joel Miller")


def test_launches_assignation_with_type(driver):
    signal = ValueMatcherProbe("ISNI assignation launched", "individual")
    _ = show_dialog(on_assign=signal.received)
    driver.select_individual()
    driver.click_ok()
    driver.check(signal)


def test_starts_progress_indicator_and_disables_ok_button_on_assignation_start(driver):
    dialog = show_dialog()
    driver.has_stopped_progress_indicator()
    dialog.assignation_in_progress()
    driver.has_ok_button_disabled()
    driver.is_showing_progress_indicator()


def test_stops_progress_indicator_and_accepts_dialog_when_assignation_succeeds(driver):
    dialog = show_dialog()

    dialog.assignation_in_progress()
    driver.is_showing_progress_indicator()

    dialog.assignation_succeeded()
    driver.has_stopped_progress_indicator()
    driver.is_hidden()


def test_hides_error_messages_by_default(driver):
    _ = show_dialog()
    driver.shows_connection_error_message(visible=False)
    driver.shows_insufficient_error_message(visible=False)


def test_stops_progress_indicator_and_displays_connection_error_message(driver):
    dialog = show_dialog()

    dialog.assignation_in_progress()
    driver.is_showing_progress_indicator()

    dialog.connection_failed()
    driver.has_stopped_progress_indicator()
    driver.has_ok_button_enabled()
    driver.shows_connection_error_message()


def test_stops_progress_indicator_and_displays_insufficient_information_message(driver):
    dialog = show_dialog()

    dialog.assignation_in_progress()
    driver.is_showing_progress_indicator()

    dialog.insufficient_information()
    driver.has_stopped_progress_indicator()
    driver.has_ok_button_enabled()
    driver.shows_insufficient_error_message()
