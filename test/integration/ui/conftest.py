# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication
import pytest


@pytest.yield_fixture()
def app():
    qt = QApplication([])
    yield qt
    qt.quit()