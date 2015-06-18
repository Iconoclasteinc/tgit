# -*- coding: utf-8 -*-
import pytest

from cute.probes import ValueMatcherProbe
from cute.finders import WidgetIdentity
from test.drivers import WelcomePageDriver
from tgit.album import Album
from tgit.ui.welcome_page import WelcomePage


@pytest.fixture()
def select_album():
    def on_select_album(callback):
        callback()

    return on_select_album


@pytest.fixture()
def page(qt, select_album):
    welcome_page = WelcomePage(select_album=select_album)
    welcome_page.show()
    return welcome_page


@pytest.yield_fixture()
def driver(page, prober, automaton):
    page_driver = WelcomePageDriver(WidgetIdentity(page), prober, automaton)
    yield page_driver
    page_driver.close()


def test_signals_when_new_mp3_album_button_clicked(page, driver):
    new_album_signal = ValueMatcherProbe("new album", Album.Type.MP3)
    page.on_create_album(new_album_signal.received)

    driver.new_album(of_type=Album.Type.MP3)
    driver.check(new_album_signal)


def test_signals_when_new_flac_album_button_clicked(page, driver):
    new_album_signal = ValueMatcherProbe("new album", Album.Type.FLAC)
    page.on_create_album(new_album_signal.received)

    driver.new_album(of_type=Album.Type.FLAC)
    driver.check(new_album_signal)


def test_signals_when_load_album_button_clicked(page, driver):
    load_album_signal = ValueMatcherProbe("load album")
    page.on_load_album(load_album_signal.received)

    driver.load()
    driver.check(load_album_signal)
