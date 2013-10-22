# -*- coding: utf-8 -*-

import os
from PyQt4.QtGui import QPushButton, QFileDialog, QWidget, QMenuBar

import tgit.ui.main_window as main
import tgit.ui.album_panel as album
import tgit.ui.track_panel as track
import tgit.ui.track_list_panel as content

from test.cute.matchers import named, showingOnScreen
from test.cute.widgets import (MainWindowDriver, AbstractButtonDriver, FileDialogDriver,
                                MenuBarDriver)
from test.drivers.track_list_panel_driver import TrackListPanelDriver
from test.drivers.album_panel_driver import AlbumPanelDriver
from test.drivers.track_panel_driver import TrackPanelDriver

DURATION = 'duration'
BITRATE = 'bitrate'
ISRC = 'isrc'
VERSION_INFO = 'versionInfo'
FEATURED_GUEST = 'featuredGuest'
TRACK_TITLE = 'trackTitle'


class TaggerDriver(MainWindowDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(TaggerDriver, self).__init__(selector, prober, gesturePerformer)

    def importTrack(self, path):
        self.selectImportTrackMenuItem()
        self.selectTrack(path)
        self.isShowingTrackList()

    def selectImportTrackMenuItem(self):
        menuItem = self._importTrackMenuItem()
        menuItem.isEnabled()
        menuItem.click()

    def _importTrackMenuItem(self):
        menu = self._fileMenu()
        menu.open()
        return menu.menuItem(named(main.IMPORT_TRACK_ACTION_NAME))

    def selectTrack(self, trackFile):
        dialog = FileDialogDriver.findIn(self, QFileDialog, named(main.IMPORT_TRACK_DIALOG_NAME))
        dialog.showHiddenFiles()
        dialog.navigateToDir(os.path.dirname(trackFile))
        dialog.selectFile(os.path.basename(trackFile))
        dialog.accept()

    def addTrack(self):
        self._trackListPanel().addTrack()

    def createAlbum(self):
        self._newAlbumButton().click()

    # todo when we have our custom welcome panel, check that the panel is displayed
    def isShowingWelcomePanel(self):
        self._newAlbumButton().isShowingOnScreen()

    def isShowingTrackList(self):
        self._trackListPanel().isShowingOnScreen()
        self._nextStepButton().isEnabled()
        self._previousStepButton().isDisabled()
        self._saveButton().isDisabled()
        self._importTrackMenuItem().isEnabled()
        self._fileMenu().close()

    def isShowingAlbumMetadata(self):
        self._albumPanel().isShowingOnScreen()
        self._nextStepButton().isEnabled()
        self._previousStepButton().isEnabled()
        self._saveButton().isEnabled()

    def isShowingTrackMetadata(self):
        self._currentTrackPanel().isShowingOnScreen()
        self._previousStepButton().isEnabled()
        self._saveButton().isEnabled()

    def nextPage(self):
        button = self._nextStepButton()
        button.isEnabled()
        button.click()

    def previousPage(self):
        button = self._previousStepButton()
        button.isEnabled()
        button.click()

    def hasNextStepDisabled(self):
        self._nextStepButton().isDisabled()

    def removeTrack(self, title):
        self.isShowingTrackList()
        self._trackListPanel().removeTrack(title)

    def moveTrack(self, title, whereTitle):
        self.isShowingTrackList()
        self._trackListPanel().moveTrack(title, whereTitle)

    # todo have a quick navigation button
    def navigateToAlbumMetadata(self):
        self.nextPage()
        self.isShowingAlbumMetadata()

    # todo have a quick navigation button
    def navigateToTrackMetadata(self):
        self.nextPage()
        self.isShowingTrackMetadata()

    def showsAlbumContains(self, *tracks):
        trackList = self._trackListPanel()
        for track in tracks:
            trackList.showsTrack(*track)

    def showsAlbumMetadata(self, **tags):
        self._albumPanel().showsMetadata(**tags)

    def editAlbumMetadata(self, **tags):
        self._albumPanel().changeMetadata(**tags)

    def showsTrackMetadata(self, **tags):
        self._currentTrackPanel().showsMetadata(**tags)

    def editTrackMetadata(self, **tags):
        self._currentTrackPanel().changeMetadata(**tags)

    def saveAlbum(self):
        self._saveButton().click()

    def _menuBar(self):
        return MenuBarDriver.findIn(self, QMenuBar)

    def _fileMenu(self):
        return self._menuBar().menu(named(main.FILE_MENU_NAME))

    def _newAlbumButton(self):
        return AbstractButtonDriver.findIn(self, QPushButton, named(main.NEW_ALBUM_BUTTON_NAME))

    def _nextStepButton(self):
        return AbstractButtonDriver.findIn(self, QPushButton, named(main.NEXT_STEP_BUTTON_NAME))

    def _previousStepButton(self):
        return AbstractButtonDriver.findIn(self, QPushButton, named(main.PREVIOUS_STEP_BUTTON_NAME))

    def _saveButton(self):
        return AbstractButtonDriver.findIn(self, QPushButton, named(main.SAVE_BUTTON_NAME))

    def _trackListPanel(self):
        trackListPanel = TrackListPanelDriver.findIn(self, QWidget,
                                                     named(content.ALBUM_CONTENT_PANEL_NAME))
        trackListPanel.isShowingOnScreen()
        return trackListPanel

    def _albumPanel(self):
        return AlbumPanelDriver.findIn(self, QWidget, named(album.ALBUM_PANEL_NAME))

    def _currentTrackPanel(self):
        return TrackPanelDriver.findIn(self, QWidget, named(track.TRACK_PANEL_NAME),
                                       showingOnScreen())