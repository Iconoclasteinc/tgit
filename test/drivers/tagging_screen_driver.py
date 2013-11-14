# -*- coding: utf-8 -*-

from PyQt4.QtGui import QWidget, QPushButton

from test.cute.widgets import WidgetDriver, ButtonDriver
from test.cute.matchers import named, showingOnScreen
from test.drivers.track_list_page_driver import TrackListPageDriver
from test.drivers.album_page_driver import AlbumPageDriver
from test.drivers.track_page_driver import TrackPageDriver

from tgit.ui import constants as ui


class TaggingScreenDriver(WidgetDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(TaggingScreenDriver, self).__init__(selector, prober, gesturePerformer)

    def isShowingTrackList(self):
        self._trackListPage().isShowingOnScreen()
        self._nextPageButton().isEnabled()
        self._previousPageButton().isDisabled()
        self._saveButton().isDisabled()

    def isShowingAlbumMetadata(self):
        self._albumPage().isShowingOnScreen()
        self._previousPageButton().isEnabled()
        self._saveButton().isEnabled()

    def isShowingTrackMetadata(self):
        self._currentTrackPage().isShowingOnScreen()
        self._previousPageButton().isEnabled()
        self._saveButton().isEnabled()

    def addFiles(self):
        self._trackListPage().addFiles()

    def removeTrack(self, title):
        self._trackListPage().removeTrack(title)

    def moveTrack(self, title, to):
        self._trackListPage().moveTrack(title, to)

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
        trackList = self._trackListPage()
        trackList.isShowingOnScreen()
        trackList.showsTracksInOrder(*tracks)

    def showsAlbumMetadata(self, **tags):
        self._albumPage().isShowingOnScreen()
        self._albumPage().showsMetadata(**tags)

    def editAlbumMetadata(self, **tags):
        self._albumPage().changeMetadata(**tags)

    def showsTrackMetadata(self, **tags):
        self._currentTrackPage().isShowingOnScreen()
        self._currentTrackPage().showsMetadata(**tags)

    def editTrackMetadata(self, **tags):
        self._currentTrackPage().changeMetadata(**tags)

    def _trackListPage(self):
        return TrackListPageDriver.findSingle(self, QWidget, named(ui.TRACK_LIST_PAGE_NAME))

    def _albumPage(self):
        return AlbumPageDriver.findSingle(self, QWidget, named(ui.ALBUM_PAGE_NAME))

    def _currentTrackPage(self):
        return TrackPageDriver.findSingle(self, QWidget, named(ui.TRACK_PAGE_NAME),
                                          showingOnScreen())

    def _nextPageButton(self):
        return ButtonDriver.findSingle(self, QPushButton, named(ui.NEXT_PAGE_BUTTON_NAME))

    def _previousPageButton(self):
        return ButtonDriver.findSingle(self, QPushButton,
                                               named(ui.PREVIOUS_PAGE_BUTTON_NAME))

    def _saveButton(self):
        return ButtonDriver.findSingle(self, QPushButton, named(ui.SAVE_BUTTON_NAME))
