# -*- coding: utf-8 -*-

from hamcrest import assert_that, equal_to
import pytest

from cute.finders import WidgetIdentity
from cute.prober import EventProcessingProber
from cute.probes import ValueMatcherProbe
from cute.robot import Robot
from test.drivers import SettingsDialogDriver
from tgit.ui import SettingsDialog


@pytest.fixture()
def dialog(main_window):
    return SettingsDialog(main_window)


@pytest.yield_fixture()
def driver(dialog):
    dialog_driver = SettingsDialogDriver(WidgetIdentity(dialog), EventProcessingProber(), Robot())
    yield dialog_driver
    dialog_driver.close()


def test_displays_user_preferences(dialog, driver):
    dialog.add_language('en', 'English')
    dialog.add_language('fr', 'French')
    dialog.display(language='fr')
    dialog.open()

    driver.shows_language('French')


def test_offers_selection_of_available_languages(dialog, driver):
    dialog.add_language('en', 'English')
    dialog.add_language('fr', 'French')
    assert_that(dialog.settings['language'], equal_to('en'), 'default language')

    dialog.open()

    driver.shows_language('English')
    driver.select_language('French')
    driver.shows_language('French')
    assert_that(dialog.settings['language'], equal_to('fr'), 'selected language')


def test_signals_when_selection_accepted(dialog, driver):
    dialog.add_language('en', 'English')
    accepted_signal = ValueMatcherProbe("click on button 'OK'")
    dialog.accepted.connect(accepted_signal.received)

    dialog.open()

    driver.ok()
    driver.check(accepted_signal)


def test_signals_when_selection_rejected(dialog, driver):
    dialog.add_language('en', 'English')
    rejected_signal = ValueMatcherProbe("click on button 'Cancel'")
    dialog.rejected.connect(rejected_signal.received)

    dialog.open()

    driver.cancel()
    driver.check(rejected_signal)

