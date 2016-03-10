import pytest
from PyQt5.QtCore import Qt

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers.isni_assignation_review_dialog_driver import IsniAssignationReviewDialogDriver
from test.util import builders as build
from tgit import platforms
from tgit.ui.dialogs.isni_assignation_review_dialog import ISNIAssignationReviewDialog

pytestmark = pytest.mark.ui

ANIMATION_DELAY = 200 if platforms.mac else 0


def ignore(*_):
    pass


def show_dialog(*titles, main_artist_section_visible=True, on_review=ignore):
    dialog = ISNIAssignationReviewDialog(main_artist_section_visible=main_artist_section_visible)
    dialog.setAttribute(Qt.WA_DeleteOnClose, False)
    dialog.review(on_review, *titles)
    return dialog


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    dialog_driver = IsniAssignationReviewDialogDriver(
        window(ISNIAssignationReviewDialog, named("isni_assignation_review_dialog")), prober, automaton)
    yield dialog_driver
    dialog_driver.close()


def test_signals_organization_type_on_accept(driver):
    review_signal = ValueMatcherProbe("assignation review", "organization")

    _ = show_dialog(on_review=review_signal.received)

    driver.pause(ANIMATION_DELAY)
    driver.select_organization()
    driver.click_ok()
    driver.check(review_signal)


def test_signals_individual_type_on_accept(driver):
    review_signal = ValueMatcherProbe("assignation review", "individual")

    _ = show_dialog(on_review=review_signal.received)

    driver.pause(ANIMATION_DELAY)
    driver.select_individual()
    driver.click_ok()
    driver.check(review_signal)


def test_displays_works(driver):
    _ = show_dialog(build.track(track_title="My title"), on_review=ignore)
    driver.has_work("My title")


def test_shows_main_artist_section(driver):
    _ = show_dialog(main_artist_section_visible=True)
    driver.shows_main_artist_section()


def test_hides_main_artist_section(driver):
    _ = show_dialog(main_artist_section_visible=False)
    driver.hides_main_artist_section()
