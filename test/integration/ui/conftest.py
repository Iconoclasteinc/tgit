# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication
import pytest


@pytest.yield_fixture()
def qt():
    app = QApplication([])
    yield app
    app.quit()