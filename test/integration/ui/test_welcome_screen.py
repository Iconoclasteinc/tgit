# -*- coding: utf-8 -*-
import pytest

from cute.probes import ValueMatcherProbe
from cute.finders import WidgetIdentity
from test.drivers import WelcomeScreenDriver
from tgit.album import Album
from tgit.ui.welcome_screen import WelcomeScreen


@pytest.fixture()
def screen(main_window):
    welcome_screen = WelcomeScreen()
    main_window.setCentralWidget(welcome_screen)
    return welcome_screen


@pytest.yield_fixture()
def driver(screen, prober, automaton):
    screen_driver = WelcomeScreenDriver(WidgetIdentity(screen), prober, automaton)
    yield screen_driver
    screen_driver.close()


def test_signals_when_new_mp3_album_button_clicked(screen, driver):
    new_album_signal = ValueMatcherProbe("new album", Album.Type.MP3)
    screen.create_new_album.connect(new_album_signal.received)

    driver.new_album(of_type=Album.Type.MP3)
    driver.check(new_album_signal)


def test_signals_when_new_flac_album_button_clicked(screen, driver):
    new_album_signal = ValueMatcherProbe("new album", Album.Type.FLAC)
    screen.create_new_album.connect(new_album_signal.received)

    driver.new_album(of_type=Album.Type.FLAC)
    driver.check(new_album_signal)


def test_signals_when_import_album_button_clicked(screen, driver):
    import_album_signal = ValueMatcherProbe("import album")
    screen.import_album.connect(import_album_signal.received)

    driver.import_album()
    driver.check(import_album_signal)