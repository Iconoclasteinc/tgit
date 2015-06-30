# -*- coding: utf-8 -*-
import sip

from PyQt5.QtWidgets import QApplication
import pytest

from cute.animatron import Animatron
from cute.prober import EventProcessingProber
from cute.robot import Robot


@pytest.yield_fixture(autouse=True)
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
