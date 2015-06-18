# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from hamcrest import assert_that, equal_to
import pytest

from cute.finders import WidgetIdentity
from cute.probes import ValueMatcherProbe
from test.drivers import PerformerDialogDriver
from test.integration.ui import show_widget
from tgit.ui import PerformerDialog

DISPLAY_DELAY = 200


@pytest.fixture()
def dialog(qt):
    dialog = PerformerDialog()
    dialog.setAttribute(Qt.WA_DeleteOnClose, False)
    show_widget(dialog)
    return dialog


@pytest.yield_fixture()
def driver(dialog, prober, automaton):
    dialog_driver = PerformerDialogDriver(WidgetIdentity(dialog), prober, automaton)
    dialog_driver.pause(DISPLAY_DELAY)
    yield dialog_driver
    dialog_driver.close()


def test_adds_performers(dialog, driver):
    dialog.display(performers=())

    driver.change_instrument('Guitar', index=0)
    driver.change_performer_name('Jimmy Page', index=0)
    driver.add_performer()

    driver.change_instrument('Vocals', index=1)
    driver.change_performer_name('Robert Plant', index=1)

    performers = dialog.getPerformers()
    assert_that(performers, equal_to([('Guitar', 'Jimmy Page'), ('Vocals', 'Robert Plant')]), 'performers')


def test_removes_performers(dialog, driver):
    dialog.display(performers=(('Guitar', 'Jimmy Page'), ('Vocals', 'Robert Plant')))

    driver.remove_performer(1)

    performers = dialog.getPerformers()
    assert_that(performers, equal_to([('Guitar', 'Jimmy Page')]), 'performers')


def test_shows_performers(dialog, driver):
    dialog.display(performers=(('Guitar', 'Jimmy Page'), ('Vocals', 'Robert Plant')))

    driver.shows_performers((('Guitar', 'Jimmy Page'), ('Vocals', 'Robert Plant')))


def test_signals_when_accepted(dialog, driver):
    accepted_signal = ValueMatcherProbe("click on button 'OK'")
    dialog.accepted.connect(accepted_signal.received)

    driver.ok()
    driver.check(accepted_signal)


def test_signals_when_rejected(dialog, driver):
    rejected_signal = ValueMatcherProbe("click on button 'Cancel'")

    dialog.rejected.connect(rejected_signal.received)

    driver.cancel()
    driver.check(rejected_signal)
