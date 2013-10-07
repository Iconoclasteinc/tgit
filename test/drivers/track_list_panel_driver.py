# -*- coding: utf-8 -*-

from PyQt4.QtGui import QPushButton, QTableWidget
from hamcrest import contains, has_items

from tgit.ui import track_list_panel as ui

from test.cute.widgets import WidgetDriver, AbstractButtonDriver, TableDriver
from test.cute.matchers import named, withText


class TrackListPanelDriver(WidgetDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(TrackListPanelDriver, self).__init__(selector, prober, gesturePerformer)

    def showsColumnHeaders(self, *titles):
        headersMatching = [withText(title) for title in titles]
        self._trackTable().hasHeading(contains(*headersMatching))

    def showsTrack(self, *details):
        cellsMatching = [withText(detail) for detail in details]
        self._trackTable().hasRow(has_items(*cellsMatching))

    def isPlayingTrack(self, track):
        self._playButton(track).isDown()

    def isNotPlayingTrack(self, track):
        self._playButton(track).isUp()

    def clickPlayButton(self, track):
        row, column = self._listenCell(track)
        self._trackTable().clickOnCell(row, column)

    def playTrack(self, track):
        self.isNotPlayingTrack(track)
        # We can't just click on the button, it's not aware of its position in the table
        self.clickPlayButton(track)
        self.isPlayingTrack(track)

    def stopTrack(self, track):
        self.isPlayingTrack(track)
        # We can't just click on the button, it's not aware of its position in the table
        self.clickPlayButton(track)
        self.isNotPlayingTrack(track)

    def addTrack(self):
        button = AbstractButtonDriver.findIn(self, QPushButton, named(ui.ADD_BUTTON_NAME))
        button.click()

    def _trackTable(self):
        return TableDriver.findIn(self, QTableWidget, named(ui.TRACK_TABLE_NAME))

    def _playButton(self, track):
        row, column = self._listenCell(track)
        button = AbstractButtonDriver.findIn(self._trackTable().widgetInCell(row, column),
                                             QPushButton, named(ui.PLAY_BUTTON_NAME))
        button.isShowingOnScreen()
        return button

    def _listenCell(self, track):
        return track - 1, ui.LISTEN