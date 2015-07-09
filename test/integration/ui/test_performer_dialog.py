# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from hamcrest import assert_that, equal_to
import pytest
import sys

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers import PerformerDialogDriver
from test.integration.ui import show_widget
from tgit.ui import PerformerDialog

mac = sys.platform == "darwin"

DISPLAY_DELAY = 200 if mac else 0


def show_dialog():
    dialog = PerformerDialog()
    dialog.setAttribute(Qt.WA_DeleteOnClose, False)
    show_widget(dialog)
    return dialog


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    dialog_driver = PerformerDialogDriver(window(PerformerDialog, named("performers_dialog")), prober, automaton)
    dialog_driver.pause(DISPLAY_DELAY)
    yield dialog_driver
    dialog_driver.close()


def test_adds_performers(driver):
    dialog = show_dialog()
    dialog.display(performers=())

    driver.change_instrument("Guitar", index=0)
    driver.change_performer_name("Jimmy Page", index=0)
    driver.add_performer()

    driver.change_instrument("Vocals", index=1)
    driver.change_performer_name("Robert Plant", index=1)

    assert_that(dialog.get_performers(), equal_to([("Guitar", "Jimmy Page"), ("Vocals", "Robert Plant")]), "performers")


def test_removes_performers(driver):
    dialog = show_dialog()
    dialog.display(performers=(("Guitar", "Jimmy Page"), ("Vocals", "Robert Plant")))

    driver.remove_performer(1)

    assert_that(dialog.get_performers(), equal_to([("Guitar", "Jimmy Page")]), "performers")


def test_shows_performers(driver):
    dialog = show_dialog()
    dialog.display(performers=(("Guitar", "Jimmy Page"), ("Vocals", "Robert Plant")))

    driver.shows_performers((("Guitar", "Jimmy Page"), ("Vocals", "Robert Plant")))


def test_signals_when_accepted(driver):
    dialog = show_dialog()
    accepted_signal = ValueMatcherProbe("click on button 'OK'")
    dialog.accepted.connect(accepted_signal.received)

    driver.ok()
    driver.check(accepted_signal)


def test_signals_when_rejected(driver):
    dialog = show_dialog()
    rejected_signal = ValueMatcherProbe("click on button 'Cancel'")

    dialog.rejected.connect(rejected_signal.received)

    driver.cancel()
    driver.check(rejected_signal)
