# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication
import pytest
from cute import event_loop
from cute.animatron import Animatron
from cute.prober import EventProcessingProber
from cute.robot import Robot
from test.integration.ui import show_widget
from tgit.ui.main_window import MainWindow

INITIAL_DISPLAY_TIME = 100  # time for main window to display its central widget


@pytest.yield_fixture()
def qt():
    app = QApplication([])
    yield app
    event_loop.process_pending_events()
    app.quit()


@pytest.yield_fixture()
def main_window(qt):
    window = MainWindow(create_startup_screen=lambda: None, create_album_screen=lambda: None)
    show_widget(window)
    yield window
    window.close()


@pytest.fixture()
def prober():
    event_processor = EventProcessingProber()
    event_loop.process_events_for(INITIAL_DISPLAY_TIME)
    return event_processor


@pytest.fixture()
def automaton():
    return Animatron()


@pytest.fixture()
def robot():
    return Robot()


@pytest.fixture()
def animaton():
    return Animatron()
