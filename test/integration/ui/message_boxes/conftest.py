import pytest
from PyQt5.QtWidgets import QMessageBox

from cute.matchers import named
from cute.widgets import QMessageBoxDriver
from cute.widgets import window


@pytest.fixture()
def driver(prober, automaton):
    return QMessageBoxDriver(window(QMessageBox, named("message_box")), prober, automaton)