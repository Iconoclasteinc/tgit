# -*- coding: utf-8 -*-
import sys

from PyQt5.QtCore import Qt
from hamcrest import contains
import pytest

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers import PerformerDialogDriver
from test.util import builders as build
from tgit.platforms import mac
from tgit.ui.dialogs.performer_dialog import PerformerDialog

ignore = lambda *_: None

DISPLAY_DELAY = 200 if mac else 0


def show_dialog(album=build.album(guest_performers=[]), on_edit=ignore):
    dialog = PerformerDialog(album)
    dialog.setAttribute(Qt.WA_DeleteOnClose, False)
    dialog.edit(on_edit=on_edit)
    return dialog


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    dialog_driver = PerformerDialogDriver(window(PerformerDialog, named("performers_dialog")), prober, automaton)
    yield dialog_driver
    dialog_driver.close()


def test_adds_performers(driver):
    _ = show_dialog()

    driver.pause(DISPLAY_DELAY)
    driver.add_performer(instrument="Guitar", name="Jimmy Page", row=1)
    driver.add_performer(instrument="Vocals", name="Robert Plant", row=2)
    driver.ok()


def test_shows_performers(driver):
    _ = show_dialog(album=build.album(guest_performers=[("Guitar", "Jimmy Page"), ("Vocals", "Robert Plant")]))

    driver.shows_performers(("Guitar", "Jimmy Page"), ("Vocals", "Robert Plant"))


def test_removes_performers(driver):
    _ = show_dialog(album=build.album(guest_performers=[("Guitar", "Jimmy Page"), ("Vocals", "Robert Plant")]))

    driver.remove_performer(row=2)
    driver.shows_performers(("Guitar", "Jimmy Page"))


def test_signals_when_accepted(driver):
    accepted_signal = ValueMatcherProbe("accepted performers",
                                        contains(contains("Guitar", "Jimmy Page"), contains("Vocals", "Robert Plant")))
    _ = show_dialog(album=build.album(guest_performers=[("Guitar", "Jimmy Page"), ("Vocals", "Robert Plant")]),
                    on_edit=accepted_signal.received)

    driver.pause(DISPLAY_DELAY)
    driver.ok()
    driver.check(accepted_signal)
