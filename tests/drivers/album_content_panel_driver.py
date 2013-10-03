# -*- coding: utf-8 -*-

from PyQt4.QtGui import QWidget, QLabel, QPushButton
from hamcrest import contains_string, starts_with

from tgit.ui import album_content_panel as ui

from tests.cute.widgets import WidgetDriver, LabelDriver, AbstractButtonDriver
from tests.cute.matchers import named, withLabelText, withButtonText


class AlbumContentPanelDriver(WidgetDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(AlbumContentPanelDriver, self).__init__(selector, prober, gesturePerformer)

    def showsColumnHeadings(self, *headings):
        header = WidgetDriver.findIn(self, QWidget, named(ui.TRACK_TABLE_HEADER_NAME))
        for column, heading in enumerate(headings):
            cell = LabelDriver.nthIn(header, QLabel, column)
            cell.hasText(contains_string(heading))

    def row(self, index):
        return WidgetDriver.nthIn(self, QWidget, index - 1,
                                  named(starts_with(ui.TRACK_TABLE_ROW_NAME)))

    def showsTrackDetails(self, index, *details):
        for column, content in enumerate(details):
            cell = LabelDriver.nthIn(self.row(index), QLabel, column)
            cell.hasText(content)

    def playTrack(self, index):
        button = self.playButton(index)
        button.isUp()
        button.click()
        button.isDown()

    def playButton(self, index):
        button = AbstractButtonDriver.findIn(self.row(index), QPushButton, withButtonText('Play'))
        button.isShowingOnScreen()
        return button

    def stopTrack(self, index):
        button = self.playButton(index)
        button.isDown()
        button.click()
        button.isUp()