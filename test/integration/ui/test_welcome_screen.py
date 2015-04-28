# -*- coding: utf-8 -*-
import pytest
from cute.prober import EventProcessingProber

from cute.probes import ValueMatcherProbe
from cute.finders import WidgetIdentity
from cute.robot import Robot
from test.drivers import WelcomeScreenDriver
from test.integration.ui import show_widget

from tgit.ui.welcome_screen import WelcomeScreen

@pytest.fixture()
def welcome_screen(qt):
    screen = WelcomeScreen()
    show_widget(screen)
    return screen


@pytest.yield_fixture()
def driver(welcome_screen):
    screen_driver = WelcomeScreenDriver(WidgetIdentity(welcome_screen), EventProcessingProber(), Robot())
    yield screen_driver
    screen_driver.close()


def test_signals_when_new_album_button_clicked(welcome_screen, driver):
    new_album_signal = ValueMatcherProbe('new album')
    welcome_screen.newAlbum.connect(new_album_signal.received)

    driver.new_album()
    driver.check(new_album_signal)