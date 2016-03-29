# -*- coding: utf-8 -*-
import pytest

from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers.isni_assignation_review_dialog_driver import IsniAssignationReviewDialogDriver
from test.ui import ignore, show_, close_
from test.util.builders import make_album, make_track
from tgit.identity import IdentitySelection
from tgit.ui import make_isni_assignation_review_dialog
from tgit.ui.dialogs.isni_assignation_review_dialog import ISNIAssignationReviewDialog

pytestmark = pytest.mark.ui


def show_dialog(isni_selection=IdentitySelection(make_album(), ""), on_assign=ignore, main_artist_section_visible=True):
    dialog = make_isni_assignation_review_dialog(isni_selection, on_assign,
                                                 main_artist_section_visible=main_artist_section_visible,
                                                 delete_on_close=False)
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


def test_shows_main_artist_section(driver):
    _ = show_dialog(main_artist_section_visible=True)
    driver.shows_main_artist_section()


def test_hides_main_artist_section(driver):
    _ = show_dialog(main_artist_section_visible=False)
    driver.hides_main_artist_section()


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
