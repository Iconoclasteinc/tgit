# -*- coding: utf-8 -*-
from hamcrest import instance_of
import pytest

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers import WelcomePageDriver
from tgit.ui.pages.welcome_page import WelcomePage

ignore = lambda: None


def show_page(select_album=ignore, show_load_error=ignore, **handlers):
    welcome_page = WelcomePage(select_album, show_load_error, **handlers)
    welcome_page.show()
    return welcome_page


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    page_driver = WelcomePageDriver(window(WelcomePage, named("welcome_page")), prober, automaton)
    yield page_driver
    page_driver.close()


def test_signals_when_new_album_button_clicked(driver):
    new_album_signal = ValueMatcherProbe("new album")
    page = show_page()
    page.on_create_album(lambda: new_album_signal.received())

    driver.new_album()
    driver.check(new_album_signal)


def test_signals_when_load_album_button_clicked(driver):
    load_album_signal = ValueMatcherProbe("load album", "album.tgit")
    page = show_page(select_album=lambda on_select: on_select("album.tgit"))
    page.on_load_album(load_album_signal.received)

    driver.load()
    driver.check(load_album_signal)


def test_warn_user_if_load_failed(driver):
    def load_fails(_):
        raise OSError("Load failed")

    load_failed_signal = ValueMatcherProbe("load album failed", instance_of(OSError))

    _ = show_page(select_album=lambda load: load("album.tgit"),
                  show_load_error=load_failed_signal.received,
                  on_load_album=load_fails)

    driver.load()
    driver.check(load_failed_signal)
