# -*- coding: utf-8 -*-

from PyQt4.QtGui import QLabel

from tgit.ui import album_content_panel as ui

from tests.cute.widgets import WidgetDriver, LabelDriver
from tests.cute.matchers import named


class AlbumContentPanelDriver(WidgetDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(AlbumContentPanelDriver, self).__init__(selector, prober, gesturePerformer)

    def showsTrackTitle(self, title):
        label = LabelDriver.find(self, QLabel, named(ui.ALBUM_TRACK_TITLE_NAME))
        label.isShowingOnScreen()
        label.hasText(title)
