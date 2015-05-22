# -*- coding: utf-8 -*-

from hamcrest import assert_that, equal_to
import pytest

from cute.finders import WidgetIdentity
from cute.prober import EventProcessingProber
from cute.probes import ValueMatcherProbe
from cute.robot import Robot
from test.drivers.performer_dialog_driver import PerformerDialogDriver
from test.integration.ui import show_widget
from tgit.ui.performer_dialog import PerformerDialog


DISPLAY_DELAY = 200


@pytest.fixture()
def performer_dialog(qt):
    dialog = PerformerDialog()
    show_widget(dialog)
    return dialog


@pytest.yield_fixture()
def driver(performer_dialog):
    driver = PerformerDialogDriver(WidgetIdentity(performer_dialog), EventProcessingProber(), Robot())
    driver.pause(DISPLAY_DELAY)
    yield driver
    driver.close()


def test_adds_performers(performer_dialog, driver):
    performer_dialog.display(performers=())

    driver.change_instrument('Guitar', index=0)
    driver.change_performer_name('Jimmy Page', index=0)
    driver.add_performer()

    driver.change_instrument('Vocals', index=1)
    driver.change_performer_name('Robert Plant', index=1)

    performers = performer_dialog.getPerformers()
    assert_that(performers, equal_to([('Guitar', 'Jimmy Page'), ('Vocals', 'Robert Plant')]), 'performers')


def test_removes_performers(performer_dialog, driver):
    performer_dialog.display(performers=(('Guitar', 'Jimmy Page'), ('Vocals', 'Robert Plant')))

    driver.remove_performer(1)

    performers = performer_dialog.getPerformers()
    assert_that(performers, equal_to([('Guitar', 'Jimmy Page')]), 'performers')


def test_shows_performers(performer_dialog, driver):
    performer_dialog.display(performers=(('Guitar', 'Jimmy Page'), ('Vocals', 'Robert Plant')))

    driver.shows_performers((('Guitar', 'Jimmy Page'), ('Vocals', 'Robert Plant')))


def test_signals_when_accepted(performer_dialog, driver):
    accepted_signal = ValueMatcherProbe("click on button 'OK'")
    performer_dialog.accepted.connect(accepted_signal.received)

    driver.ok()
    driver.check(accepted_signal)


def test_signals_when_rejected(performer_dialog, driver):
    rejected_signal = ValueMatcherProbe("click on button 'Cancel'")

    performer_dialog.rejected.connect(rejected_signal.received)

    driver.cancel()
    driver.check(rejected_signal)
