# -*- coding: utf-8 -*-
import sip

from PyQt5.QtWidgets import QApplication, QWidget
import pytest

from cute.animatron import Animatron
from cute.matchers import named
from cute.prober import EventProcessingProber
from cute.robot import Robot
from cute.widgets import window, WidgetDriver
from test.drivers import TrackEditionPageDriver
from tgit.ui.track_edition_page import TrackEditionPage


@pytest.yield_fixture()
def qt():
    app = QApplication([])
    yield app
    app.quit()
    # If we don't force deletion of the C++ wrapped object, it causes the test suite to eventually crash
    # Never ever remove this!!
    sip.delete(app)


@pytest.fixture()
def prober():
    return EventProcessingProber()


@pytest.fixture()
def automaton():
    return Animatron()


@pytest.fixture()
def robot():
    return Robot()


@pytest.fixture()
def animaton():
    return Animatron()


@pytest.fixture()
def widget_driver(qt, prober, automaton):
    return WidgetDriver(window(QWidget), prober, automaton)


@pytest.yield_fixture()
def track_edition_page_driver(qt, prober, automaton):
    page_driver = TrackEditionPageDriver(window(TrackEditionPage, named("track_edition_page")), prober, automaton)
    yield page_driver
    page_driver.close()
