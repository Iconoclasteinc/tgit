# -*- coding: utf-8 -*-

from hamcrest import contains, has_items

from PyQt4.QtGui import QPushButton, QTableWidget

from test.cute.widgets import WidgetDriver, AbstractButtonDriver, TableDriver
from test.cute.matchers import named, withText

from tgit.ui import constants as ui
from tgit.ui import track_list_page as page


class TrackListPageDriver(WidgetDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(TrackListPageDriver, self).__init__(selector, prober, gesturePerformer)

    def showsColumnHeaders(self, *titles):
        headersMatching = [withText(title) for title in titles]
        self._trackTable().hasHeading(contains(*headersMatching))

    def showsTrack(self, *columns):
        cells = [withText(column) for column in columns]
        return self._trackTable().hasRow(has_items(*cells))

    def showsTracksInOrder(self, *tracks):
        rows = [has_items(*[withText(column) for column in track]) for track in tracks]
        return self._trackTable().containsRows(contains(*rows))

    def hasTrackCount(self, count):
        self._trackTable().hasRowCount(count)

    def isPlaying(self, title):
        row = self.showsTrack(title)
        self._playButtonAt(row).isDown()

    def isNotPlaying(self, title):
        row = self.showsTrack(title)
        self._playButtonAt(row).isUp()

    def playOrStop(self, title):
        row = self.showsTrack(title)
        self._playButtonAt(row).isShowingOnScreen()
        self._clickPlayButtonAt(row)

    def play(self, title):
        self.isNotPlaying(title)
        self.playOrStop(title)
        self.isPlaying(title)

    def stopTrack(self, title):
        self.isPlaying(title)
        self.playOrStop(title)
        self.isNotPlaying(title)

    def addTrack(self):
        button = AbstractButtonDriver.findSingle(self, QPushButton, named(ui.ADD_TRACK_BUTTON_NAME))
        button.click()

    def removeTrack(self, title):
        row = self.showsTrack(title)
        self._removeButtonAt(row).isShowingOnScreen()
        self._clickRemoveButtonAt(row)

    def moveTrack(self, title, to):
        from_ = self.showsTrack(title)
        self._trackTable().moveRow(from_, to)

    def _removeButtonAt(self, row):
        return AbstractButtonDriver.findSingle(self._removeWidget(row), QPushButton,
                                               named(ui.REMOVE_BUTTON_NAME))

    def _removeWidget(self, index):
        return self._trackTable().widgetInCell(index, page.REMOVE_COLUMN)

    def _clickRemoveButtonAt(self, row):
        self._trackTable().clickOnCell(row, page.REMOVE_COLUMN)

    def _playButtonAt(self, index):
        return AbstractButtonDriver.findSingle(self._playWidget(index), QPushButton,
                                               named(ui.PLAY_BUTTON_NAME))

    def _playWidget(self, index):
        return self._trackTable().widgetInCell(index, page.PLAY_COLUMN)

    def _clickPlayButtonAt(self, row):
        self._trackTable().clickOnCell(row, page.PLAY_COLUMN)

    def _trackTable(self):
        return TableDriver.findSingle(self, QTableWidget, named(ui.TRACK_TABLE_NAME))
