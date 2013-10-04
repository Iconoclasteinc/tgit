# -*- coding: utf-8 -*-

import os
from PyQt4.QtGui import QPushButton, QFileDialog, QWidget, QMenuBar

import tgit.ui.main_window as main
import tgit.ui.album_panel as album
import tgit.ui.track_panel as track
import tgit.ui.track_list_panel as content

from tests.cute.matchers import named, showingOnScreen
from tests.cute.widgets import (MainWindowDriver, AbstractButtonDriver, FileDialogDriver,
                                MenuBarDriver)
from tests.drivers.track_list_panel_driver import TrackListPanelDriver
from tests.drivers.album_panel_driver import AlbumPanelDriver
from tests.drivers.track_panel_driver import TrackPanelDriver

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
        self.importTrackThroughMenu(path)
        self.isShowingTrackList()

    # todo having to specify how we import the track kinda sucks
    # plus, there are so many ways to import a track it's confusing
    def importTrackThroughMenu(self, path):
        self._selectImportTrackMenuItem()
        self._selectTrackInDialog(path)

    def _selectImportTrackMenuItem(self):
        menu = self._fileMenu()
        menu.open()
        menu.selectMenuItem(named(main.IMPORT_TRACK_ACTION_NAME))

    def _selectTrackInDialog(self, trackFile):
        dialog = FileDialogDriver.findIn(self, QFileDialog, named(main.IMPORT_TRACK_DIALOG_NAME))
        dialog.showHiddenFiles()
        dialog.navigateToDir(os.path.dirname(trackFile))
        dialog.selectFile(os.path.basename(trackFile))
        dialog.accept()

    def addTrackToAlbum(self, path):
        self._addTrackButton().click()
        self._selectTrackInDialog(path)

    # todo when we have our custom welcome panel, check that the panel is displayed
    def isShowingWelcomePanel(self):
        self._addTrackButton().isShowingOnScreen()

    def isShowingTrackList(self):
        self._trackListPanel().isShowingOnScreen()
        self._nextStepButton().isEnabled()
        self._previousStepButton().isDisabled()
        self._saveButton().isDisabled()

    def isShowingAlbumMetadata(self):
        self._albumPanel().isShowingOnScreen()
        self._nextStepButton().isEnabled()
        self._previousStepButton().isEnabled()
        self._saveButton().isEnabled()

    def isShowingTrackMetadata(self):
        self._currentTrackPanel().isShowingOnScreen()
        self._previousStepButton().isEnabled()
        self._saveButton().isEnabled()

    def nextStep(self):
        button = self._nextStepButton()
        button.isEnabled()
        button.click()

    def previousStep(self):
        button = self._previousStepButton()
        button.isEnabled()
        button.click()

    def hasNextStepDisabled(self):
        self._nextStepButton().isDisabled()

    # todo have a quick navigation button
    def navigateToAlbumMetadata(self):
        self.nextStep()
        self.isShowingAlbumMetadata()

    # todo have a quick navigation button
    def navigateToTrackMetadata(self):
        self.nextStep()
        self.isShowingTrackMetadata()

    def showsAlbumContains(self, *tracks):
        trackList = self._trackListPanel()
        for track in tracks:
            trackList.showsTrack(track)

    def showsAlbumMetadata(self, **tags):
        self._albumPanel().showsMetadata(**tags)

    def editAlbumMetadata(self, **tags):
        self._albumPanel().changeMetadata(**tags)

    def showsTrackMetadata(self, **tags):
        self._currentTrackPanel().showsMetadata(**tags)

    def editTrackMetadata(self, **tags):
        if TRACK_TITLE in tags:
            self._currentTrackPanel().changeTrackTitle(tags[TRACK_TITLE])
        if VERSION_INFO in tags:
            self._currentTrackPanel().changeVersionInfo(tags[VERSION_INFO])
        if FEATURED_GUEST in tags:
            self._currentTrackPanel().changeFeaturedGuest(tags[FEATURED_GUEST])
        if ISRC in tags:
            self._currentTrackPanel().changeIsrc(tags[ISRC])

    def saveAlbum(self):
        self._saveButton().click()

    def _menuBar(self):
        return MenuBarDriver.findIn(self, QMenuBar)

    def _fileMenu(self):
        return self._menuBar().menu(named(main.FILE_MENU_NAME))

    def _addTrackButton(self):
        return AbstractButtonDriver.findIn(self, QPushButton, named(main.ADD_FILE_BUTTON_NAME))

    def _nextStepButton(self):
        return AbstractButtonDriver.findIn(self, QPushButton, named(main.NEXT_STEP_BUTTON_NAME))

    def _previousStepButton(self):
        return AbstractButtonDriver.findIn(self, QPushButton, named(main.PREVIOUS_STEP_BUTTON_NAME))

    def _saveButton(self):
        return AbstractButtonDriver.findIn(self, QPushButton, named(main.SAVE_BUTTON_NAME))

    def _trackListPanel(self):
        return TrackListPanelDriver.findIn(self, QWidget, named(content.ALBUM_CONTENT_PANEL_NAME))

    def _albumPanel(self):
        return AlbumPanelDriver.findIn(self, QWidget, named(album.ALBUM_PANEL_NAME))

    def _currentTrackPanel(self):
        return TrackPanelDriver.findIn(self, QWidget, named(track.TRACK_PANEL_NAME),
                                       showingOnScreen())