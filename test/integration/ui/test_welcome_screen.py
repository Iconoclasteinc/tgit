# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMainWindow
import pytest
from cute.prober import EventProcessingProber

from cute.probes import ValueMatcherProbe
from cute.finders import WidgetIdentity
from cute.robot import Robot
from test.drivers.welcome_screen_driver import WelcomeScreenDriver
from test.integration.ui import show_widget
from tgit.album import Album

from tgit.ui.welcome_screen import WelcomeScreen


@pytest.yield_fixture()
def welcome_screen(qt):
    main_window = QMainWindow()
    screen = WelcomeScreen(main_window)
    show_widget(main_window)
    yield screen
    main_window.close()


@pytest.yield_fixture()
def driver(welcome_screen):
    screen_driver = WelcomeScreenDriver(WidgetIdentity(welcome_screen), EventProcessingProber(), Robot())
    yield screen_driver
    screen_driver.close()


def test_signals_when_new_mp3_album_button_clicked(welcome_screen, driver):
    new_album_signal = ValueMatcherProbe("new album", Album.Type.MP3)
    welcome_screen.create_new_album.connect(new_album_signal.received)

    driver.new_album(of_type=Album.Type.MP3)
    driver.check(new_album_signal)


def test_signals_when_new_flac_album_button_clicked(welcome_screen, driver):
    new_album_signal = ValueMatcherProbe("new album", Album.Type.FLAC)
    welcome_screen.create_new_album.connect(new_album_signal.received)

    driver.new_album(of_type=Album.Type.FLAC)
    driver.check(new_album_signal)


def test_signals_when_import_album_button_clicked(welcome_screen, driver):
    import_album_signal = ValueMatcherProbe("import album")
    welcome_screen.import_album.connect(import_album_signal.received)

    driver.import_album()
    driver.check(import_album_signal)