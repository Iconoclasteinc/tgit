# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from test.cute.widgets import WidgetDriver, ButtonDriver
from test.cute.matchers import named
from test.drivers.album_page_driver import albumPage
from test.drivers.track_list_page_driver import trackListPage
from test.drivers.track_page_driver import trackPage

from tgit.ui import constants as ui


def taggingScreen(parent):
    return TaggingScreenDriver.findSingle(parent, QWidget, named(ui.TAGGING_SCREEN_NAME))


class TaggingScreenDriver(WidgetDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(TaggingScreenDriver, self).__init__(selector, prober, gesturePerformer)

    def isShowingTrackList(self):
        trackListPage(self).isShowingOnScreen()
        self._isDisabled(self._previousPageButton())
        self._isDisabled(self._saveButton())

    def _isDisabled(self, button):
        button.isDisabled()
        button.hasCursorShape(Qt.ArrowCursor)

    def _isEnabled(self, button):
        button.isEnabled()
        button.hasCursorShape(Qt.PointingHandCursor)

    def isShowingAlbumMetadata(self):
        albumPage(self).isShowingOnScreen()
        self._isEnabled(self._previousPageButton())
        self._isEnabled(self._saveButton())

    def isShowingTrackMetadata(self):
        trackPage(self).isShowingOnScreen()
        self._isEnabled(self._previousPageButton())
        self._isEnabled(self._saveButton())

    def addFiles(self):
        trackListPage(self).addFiles()

    def removeTrack(self, title):
        trackListPage(self).removeTrack(title)

    def moveTrack(self, title, to):
        trackListPage(self).moveTrack(title, to)

    def nextPage(self):
        button = self._nextPageButton()
        button.isEnabled()
        button.click()

    def previousPage(self):
        button = self._previousPageButton()
        button.isEnabled()
        button.click()

    def saveAlbum(self):
        self._saveButton().click()

    def hasDisabledNextPageButton(self):
        self._nextPageButton().isDisabled()

    def navigateToAlbumMetadata(self):
        self.nextPage()
        self.isShowingAlbumMetadata()

    # todo have a quick navigation button
    def navigateToTrackMetadata(self):
        self.nextPage()
        self.isShowingTrackMetadata()

    def showsAlbumContains(self, *tracks):
        trackListPage(self).isShowingOnScreen()
        trackListPage(self).showsTracksInOrder(*tracks)

    def showsAlbumMetadata(self, **tags):
        albumPage(self).isShowingOnScreen()
        albumPage(self).showsMetadata(**tags)

    def editAlbumMetadata(self, **tags):
        albumPage(self).changeMetadata(**tags)

    def showsTrackMetadata(self, **tags):
        trackPage(self).showsMetadata(**tags)

    def editTrackMetadata(self, **tags):
        trackPage(self).changeMetadata(**tags)

    def _nextPageButton(self):
        return ButtonDriver.findSingle(self, QPushButton, named(ui.NEXT_BUTTON_NAME))

    def _previousPageButton(self):
        return ButtonDriver.findSingle(self, QPushButton, named(ui.PREVIOUS_BUTTON_NAME))

    def _saveButton(self):
        return ButtonDriver.findSingle(self, QPushButton, named(ui.SAVE_BUTTON_NAME))
