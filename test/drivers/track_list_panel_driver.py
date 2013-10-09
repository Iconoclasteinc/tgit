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

    def hasTrackCount(self, count):
        self._trackTable().hasRowCount(count)

    def isPlayingTrack(self, index):
        self._showingPlayButton(index).isDown()

    # todo use track titles instead of indexes
    def isNotPlayingTrack(self, index):
        self._showingPlayButton(index).isUp()

    def clickPlayButton(self, index):
        self._trackTable().clickOnCell(index, ui.LISTEN)

    def playTrack(self, index):
        self.isNotPlayingTrack(index)
        # We can't just click on the button, it's not aware of its position in the table
        self.clickPlayButton(index)
        self.isPlayingTrack(index)

    def stopTrack(self, index):
        self.isPlayingTrack(index)
        # We can't just click on the button, it's not aware of its position in the table
        self.clickPlayButton(index)
        self.isNotPlayingTrack(index)

    def addTrack(self):
        button = AbstractButtonDriver.findIn(self, QPushButton, named(ui.ADD_BUTTON_NAME))
        button.click()

    def removeTrack(self, title):
        trackNumber = self._trackTable().hasRow(has_items(withText(title)))
        self.removeTrackAt(trackNumber)

    # todo use removeTrack(details) in test and make this one private
    def removeTrackAt(self, index):
        self._showingRemoveTrackButton(index)
        self._trackTable().clickOnCell(index, ui.REMOVE)

    def _showingRemoveTrackButton(self, index):
        button = AbstractButtonDriver.findIn(self._trackTable().widgetInCell(index, ui.REMOVE),
                                             QPushButton, named(ui.REMOVE_BUTTON_NAME))
        button.isShowingOnScreen()
        return button

    def _trackTable(self):
        return TableDriver.findIn(self, QTableWidget, named(ui.TRACK_TABLE_NAME))

    def _showingPlayButton(self, index):
        button = AbstractButtonDriver.findIn(self._trackTable().widgetInCell(index, ui.LISTEN),
                                             QPushButton, named(ui.PLAY_BUTTON_NAME))
        button.isShowingOnScreen()
        return button