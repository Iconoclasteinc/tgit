# -*- coding: utf-8 -*-

from PyQt4.QtGui import QLabel
from hamcrest.library import contains_string

from tgit.ui import album_content_panel as ui

from tests.cute.widgets import WidgetDriver, LabelDriver
from tests.cute.matchers import named, withLabelText


class AlbumContentPanelDriver(WidgetDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(AlbumContentPanelDriver, self).__init__(selector, prober, gesturePerformer)

    def showsTrackTitle(self, title):
        label = LabelDriver.find(self, QLabel, withLabelText(title))
        label.isShowingOnScreen()

    def showsColumnHeadings(self, *headings):
        label = LabelDriver.find(self, QLabel, named(ui.TRACK_TITLE_HEADER_NAME))
        label.hasText(contains_string(headings[0]))
