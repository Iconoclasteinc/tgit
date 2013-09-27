# -*- coding: utf-8 -*-

from PyQt4.QtGui import QLabel, QLineEdit

from tests.cute.matchers import named, withBuddy
from tests.cute.widgets import WidgetDriver, LabelDriver, LineEditDriver

import tgit.ui.album_panel as ui


class AlbumPanelDriver(WidgetDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(AlbumPanelDriver, self).__init__(selector, prober, gesturePerformer)

    def showsReleaseName(self, name):
        label = LabelDriver.find(self, QLabel, withBuddy(named(ui.RELEASE_NAME_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.find(self, QLineEdit, named(ui.RELEASE_NAME_NAME))
        edit.hasText(name)
