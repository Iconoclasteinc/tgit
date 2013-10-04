# -*- coding: utf-8 -*-

from PyQt4.QtGui import QPushButton, QTableWidget
from hamcrest import contains, has_items

from tgit.ui import track_list_panel as ui

from tests.cute.widgets import WidgetDriver, AbstractButtonDriver, TableDriver
from tests.cute.matchers import named, withText


class TrackListPanelDriver(WidgetDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(TrackListPanelDriver, self).__init__(selector, prober, gesturePerformer)

    def showsColumnHeaders(self, *titles):
        headersMatching = [withText(title) for title in titles]
        self._trackTable().hasHeading(contains(*headersMatching))

    def showsTrack(self, *details):
        cellsMatching = [withText(detail) for detail in details]
        self._trackTable().hasRow(has_items(*cellsMatching))

    def playTrack(self, track):
        button = self._playButton(track)
        button.isUp()
        # We can't just click on the button, it's not aware of its position in the table
        row, column = self._listenCell(track)
        self._trackTable().clickOnCell(row, column)
        button.isDown()

    def stopTrack(self, track):
        button = self._playButton(track)
        button.isDown()
        # We can't just click on the button, it's not aware of its position in the table
        row, column = self._listenCell(track)
        self._trackTable().clickOnCell(row, column)
        button.isUp()

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