# -*- coding: utf-8 -*-

from hamcrest import contains, has_items, equal_to
from PyQt4.QtGui import QAbstractButton, QTableView, QWidget

from test.cute.widgets import WidgetDriver, ButtonDriver, TableViewDriver
from test.cute.matchers import named
from tgit.ui.views.album_composition_model import Columns
from tgit.ui.views.album_composition_page import AlbumCompositionPage


def albumCompositionPage(parent):
    return AlbumCompositionPageDriver.findSingle(parent, QWidget, named(AlbumCompositionPage.NAME))


class AlbumCompositionPageDriver(WidgetDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(AlbumCompositionPageDriver, self).__init__(selector, prober, gesturePerformer)

    def showsColumnHeaders(self, *titles):
        headers = [title for title in titles]
        self._trackTable().hasHeaders(contains(*headers))

    def showsTrack(self, *columns):
        cells = [column for column in columns]
        return self._trackTable().hasRow(has_items(*cells))

    def showsTracksInOrder(self, *tracks):
        rows = [has_items(*[column for column in track]) for track in tracks]
        return self._trackTable().containsRows(contains(*rows))

    def hasTrackCount(self, count):
        self._trackTable().hasRowCount(equal_to(count))

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

    def addTracks(self):
        button = ButtonDriver.findSingle(self, QAbstractButton, named(AlbumCompositionPage.ADD_BUTTON_NAME))
        button.click()

    def removeTrack(self, title):
        row = self.showsTrack(title)
        self._removeButtonAt(row).isShowingOnScreen()
        self._clickRemoveButtonAt(row)

    def moveTrack(self, title, to):
        from_ = self.showsTrack(title)
        self._trackTable().moveRow(from_, to)

    def _removeButtonAt(self, row):
        return ButtonDriver.findSingle(self._removeWidget(row), QAbstractButton,
                                       named(AlbumCompositionPage.REMOVE_BUTTON_NAME))

    def _removeWidget(self, index):
        return self._trackTable().widgetInCell(index, Columns.index(Columns.remove))

    def _clickRemoveButtonAt(self, row):
        self._trackTable().clickOnCell(row, Columns.index(Columns.remove))

    def _playButtonAt(self, index):
        return ButtonDriver.findSingle(self._playWidget(index), QAbstractButton,
                                       named(AlbumCompositionPage.PLAY_BUTTON_NAME))

    def _playWidget(self, index):
        return self._trackTable().widgetInCell(index, Columns.index(Columns.play))

    def _clickPlayButtonAt(self, row):
        self._trackTable().clickOnCell(row, Columns.index(Columns.play))

    def _trackTable(self):
        return TableViewDriver.findSingle(self, QTableView, named(AlbumCompositionPage.TRACK_TABLE_NAME))
