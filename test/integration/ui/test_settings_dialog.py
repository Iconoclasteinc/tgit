# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMainWindow

from hamcrest import assert_that, equal_to
import pytest

from cute.finders import WidgetIdentity
from cute.prober import EventProcessingProber
from cute.probes import ValueMatcherProbe
from cute.robot import Robot
from test.drivers.settings_dialog_driver import SettingsDialogDriver
from test.integration.ui import show_widget
from tgit.ui.settings_dialog import SettingsDialog

ACTIVATION_DELAY = 25


@pytest.yield_fixture()
def settings_dialog(qt):
    main_window = QMainWindow()
    dialog = SettingsDialog(main_window)
    show_widget(main_window)
    dialog.show()
    yield dialog
    main_window.close()


@pytest.yield_fixture()
def driver(settings_dialog):
    driver = SettingsDialogDriver(WidgetIdentity(settings_dialog), EventProcessingProber(), Robot())
    driver.pause(ACTIVATION_DELAY)
    yield driver
    driver.close()


def test_displays_user_preferences(settings_dialog, driver):
    settings_dialog.add_language('en', 'English')
    settings_dialog.add_language('fr', 'French')
    settings_dialog.display(language='fr')

    driver.shows_language('French')


def test_offers_selection_of_available_languages(settings_dialog, driver):
    settings_dialog.add_language('en', 'English')
    settings_dialog.add_language('fr', 'French')
    assert_that(settings_dialog.settings['language'], equal_to('en'), 'default language')

    driver.shows_language('English')
    driver.select_language('French')
    driver.shows_language('French')
    assert_that(settings_dialog.settings['language'], equal_to('fr'), 'selected language')


def test_signals_when_selection_accepted(settings_dialog, driver):
    settings_dialog.add_language('en', 'English')

    accepted_signal = ValueMatcherProbe("click on button 'OK'")
    settings_dialog.accepted.connect(accepted_signal.received)

    driver.ok()
    driver.check(accepted_signal)


def test_signals_when_selection_rejected(settings_dialog, driver):
    settings_dialog.add_language('en', 'English')

    rejected_signal = ValueMatcherProbe("click on button 'Cancel'")
    settings_dialog.rejected.connect(rejected_signal.received)

    driver.cancel()
    driver.check(rejected_signal)

