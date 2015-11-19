# -*- coding: utf-8 -*-
import pytest
from PyQt5.QtCore import Qt

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers.isni_assignation_review_dialog_driver import IsniAssignationReviewDialogDriver
from test.util import builders as build
from tgit.ui import ISNIAssignationReviewDialog

ignore = lambda *_: None


def show_dialog(*titles, on_review=ignore):
    dialog = ISNIAssignationReviewDialog()
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
    review_signal = ValueMatcherProbe("authentication", "organization")

    _ = show_dialog(on_review=review_signal.received)

    driver.select_organization()
    driver.ok()
    driver.check(review_signal)


def test_signals_individual_type_on_accept(driver):
    review_signal = ValueMatcherProbe("authentication", "individual")

    _ = show_dialog(on_review=review_signal.received)

    driver.select_individual()
    driver.ok()
    driver.check(review_signal)


def test_displays_works(driver):
    _ = show_dialog(build.track(track_title="My title"), on_review=ignore)
    driver.has_work("My title")
