# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication
import pytest


# todo When all ui tests are using pytest, we'll be able to autouse this fixture
@pytest.yield_fixture()
def app():
    qt = QApplication([])
    yield qt
    qt.quit()