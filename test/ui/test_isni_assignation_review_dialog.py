import pytest

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers.isni_assignation_review_dialog_driver import IsniAssignationReviewDialogDriver
from test.ui import ignore, show_, close_
from test.util import builders as build
from tgit.ui.dialogs.isni_assignation_review_dialog import ISNIAssignationReviewDialog, \
    make_isni_assignation_review_dialog

pytestmark = pytest.mark.ui


def show_dialog(*titles, on_review=ignore, main_artist_section_visible=True):
    dialog = make_isni_assignation_review_dialog(titles, on_review,
                                                 main_artist_section_visible=main_artist_section_visible,
                                                 delete_on_close=False)
    show_(dialog)
    return dialog


@pytest.yield_fixture()
def driver(prober, automaton):
    dialog_driver = IsniAssignationReviewDialogDriver(
        window(ISNIAssignationReviewDialog, named("isni_assignation_review_dialog")), prober, automaton)
    yield dialog_driver
    close_(dialog_driver)


def test_signals_organization_type_on_accept(driver):
    review_signal = ValueMatcherProbe("assignation review", "organization")

    _ = show_dialog(on_review=review_signal.received)

    driver.select_organization()
    driver.click_ok()
    driver.check(review_signal)


def test_signals_individual_type_on_accept(driver):
    review_signal = ValueMatcherProbe("assignation review", "individual")

    _ = show_dialog(on_review=review_signal.received)

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
