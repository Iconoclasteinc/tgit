# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication
import pytest
from cute import event_loop
from cute.prober import EventProcessingProber
from cute.robot import Robot
from test.integration.ui import show_widget
from tgit.ui.main_window import MainWindow


@pytest.yield_fixture()
def qt():
    app = QApplication([])
    yield app
    app.quit()


@pytest.yield_fixture()
def main_window(qt):
    window = MainWindow()
    show_widget(window)
    yield window
    window.close()


@pytest.fixture()
def prober():
    event_processor = EventProcessingProber()
    event_loop.process_events_for(100)  # give initial time to main window to display its central widget
    return event_processor


@pytest.fixture()
def automaton():
    return Robot()
