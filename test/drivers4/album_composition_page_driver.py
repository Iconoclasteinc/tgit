# -*- coding: utf-8 -*-

from hamcrest import contains, has_items, equal_to
from PyQt4.QtGui import QAbstractButton, QWidget

from test.cute4.widgets import ButtonDriver
from test.cute4.matchers import named
from test.drivers4.__base import BaseDriver
from tgit4.ui.album_composition_model import Columns


def albumCompositionPage(parent):
    return AlbumCompositionPageDriver.findSingle(parent, QWidget, named('album-composition-page'))


class AlbumCompositionPageDriver(BaseDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(AlbumCompositionPageDriver, self).__init__(selector, prober, gesturePerformer)

    def showsColumnHeaders(self, *titles):
        headers = [title for title in titles]
        self.trackTable().hasHeaders(contains(*headers))

    def showsTrack(self, *columns):
        cells = [column for column in columns]
        return self.trackTable().hasRow(has_items(*cells))

    def showsTracksInOrder(self, *tracks):
        rows = [has_items(*[column for column in track]) for track in tracks]
        return self.trackTable().containsRows(contains(*rows))

    def hasTrackCount(self, count):
        self.trackTable().hasRowCount(equal_to(count))

    def play(self, title):
        row = self.showsTrack(title)
        self.playButtonAt(row).isShowingOnScreen()
        self.clickPlayButtonAt(row)

    def addTracks(self):
        self.button(named('add-tracks')).click()

    def removeTrack(self, title):
        row = self.showsTrack(title)
        self.removeButtonAt(row).isShowingOnScreen()
        self.clickRemoveButtonAt(row)

    def moveTrack(self, title, to):
        from_ = self.showsTrack(title)
        self.trackTable().moveRow(from_, to)

    def removeButtonAt(self, row):
        return ButtonDriver.findSingle(self.removeWidget(row), QAbstractButton, named('remove-track'))

    def removeWidget(self, index):
        return self.trackTable().widgetInCell(index, Columns.index(Columns.remove))

    def clickRemoveButtonAt(self, row):
        self.trackTable().clickOnCell(row, Columns.index(Columns.remove))

    def playButtonAt(self, index):
        return ButtonDriver.findSingle(self.playWidget(index), QAbstractButton, named('play-track'))

    def playWidget(self, index):
        return self.trackTable().widgetInCell(index, Columns.index(Columns.play))

    def clickPlayButtonAt(self, row):
        self.trackTable().clickOnCell(row, Columns.index(Columns.play))

    def trackTable(self):
        return self.table(named('track-list'))
