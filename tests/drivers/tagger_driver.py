# -*- coding: utf-8 -*-

import os
from PyQt4.QtGui import QPushButton, QFileDialog, QWidget, QLabel, QMenuBar

import tgit.ui.main_window as main
import tgit.ui.album_panel as album
import tgit.ui.track_panel as track
import tgit.ui.album_content_panel as content

from tests.cute.matchers import named, withLabelText
from tests.cute.widgets import (MainWindowDriver, AbstractButtonDriver, FileDialogDriver,
                                WidgetDriver, LabelDriver, MenuBarDriver)
from tests.drivers.album_panel_driver import AlbumPanelDriver
from tests.drivers.track_panel_driver import TrackPanelDriver

DURATION = 'duration'
BITRATE = 'bitrate'
ISRC = 'isrc'
VERSION_INFO = 'versionInfo'
FEATURED_GUEST = 'featuredGuest'
TRACK_TITLE = 'trackTitle'


# todo introduce support classes to capture common user workflows and separate workflows
# from isolated interactions, which are used in ui integration tests
class TaggerDriver(MainWindowDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(TaggerDriver, self).__init__(selector, prober, gesturePerformer)

    def importTrack(self, path):
        self.importTrackThroughMenu(path)
        self._isShowingAlbumManagementPanel()

    def _menuBar(self):
        return MenuBarDriver.findIn(self, QMenuBar)

    def _fileMenu(self):
        return self._menuBar().menu(named(main.FILE_MENU_NAME))

    def _addTrackButton(self):
        return AbstractButtonDriver.findIn(self, QPushButton, named(main.ADD_FILE_BUTTON_NAME))

    def addTrackToAlbum(self, path):
        self._addTrackButton().click()
        self._selectTrack(path)

    # todo having to specify how we import the track kinda sucks
    # plus, there are so many ways to import a track it's confusing
    def importTrackThroughMenu(self, path):
        menu = self._fileMenu()
        menu.open()
        menu.selectMenuItem(named(main.IMPORT_TRACK_ACTION_NAME))
        self._selectTrack(path)

    def _selectTrack(self, trackFile):
        dialog = FileDialogDriver.findIn(self, QFileDialog, named(main.IMPORT_TRACK_DIALOG_NAME))
        dialog.showHiddenFiles()
        dialog.navigateToDir(os.path.dirname(trackFile))
        dialog.selectFile(os.path.basename(trackFile))
        dialog.accept()

    def _isShowingAlbumManagementPanel(self):
        self._albumManagementPanel().isShowingOnScreen()
        self._nextStepButton().isEnabled()
        self._previousStepButton().isDisabled()
        self._saveButton().isDisabled()

    def _albumManagementPanel(self):
        return WidgetDriver.findIn(self, QWidget, named(content.ALBUM_CONTENT_PANEL_NAME))

    def showsAlbumContains(self, *tracks):
        albumContent = self._albumManagementPanel()
        for track in tracks:
            title = LabelDriver.findIn(albumContent, QLabel, withLabelText(track))
            title.isShowingOnScreen()

    def backToAlbumManagement(self):
        self._previousStepButton().click()
        self._albumPanel().isHidden()
        self._isShowingAlbumManagementPanel()

    def showsAlbumMetadata(self, **tags):
        self.navigateToAlbumMetadata()
        self._albumPanel().showsMetadata(**tags)

    def navigateToAlbumMetadata(self):
        self._nextStepButton().click()
        self._albumManagementPanel().isHidden()
        self._isShowingAlbumMetadataPanel()

    def _isShowingAlbumMetadataPanel(self):
        self._albumPanel().isShowingOnScreen()
        self._nextStepButton().isEnabled()
        self._previousStepButton().isEnabled()
        self._saveButton().isEnabled()

    def _albumPanel(self):
        return AlbumPanelDriver.findIn(self, QWidget, named(album.ALBUM_PANEL_NAME))

    def editAlbumMetadata(self, **tags):
        self._albumPanel().changeMetadata(**tags)

    def _nextStepButton(self):
        return AbstractButtonDriver.findIn(self, QPushButton, named(main.NEXT_STEP_BUTTON_NAME))

    def _previousStepButton(self):
        return AbstractButtonDriver.findIn(self, QPushButton, named(main.PREVIOUS_STEP_BUTTON_NAME))

    def backToAlbumMetadata(self):
        self._previousStepButton().click()
        self._trackPanel().isHidden()
        self._isShowingAlbumMetadataPanel()

    def showsTrackMetadata(self, **tags):
        self.navigateToTrackMetadata()
        self._trackPanel().showsMetadata(**tags)

    def _isShowingTrackMetadataPanel(self):
        self._trackPanel().isShowingOnScreen()
        self._previousStepButton().isEnabled()
        self._nextStepButton().isDisabled()
        self._saveButton().isEnabled()

    def navigateToTrackMetadata(self):
        self._nextStepButton().click()
        self._albumPanel().isHidden()
        self._isShowingTrackMetadataPanel()

    def _trackPanel(self):
        return TrackPanelDriver.findIn(self, QWidget, named(track.TRACK_PANEL_NAME))

    def editTrackMetadata(self, **tags):
        if TRACK_TITLE in tags:
            self._trackPanel().changeTrackTitle(tags[TRACK_TITLE])
        if VERSION_INFO in tags:
            self._trackPanel().changeVersionInfo(tags[VERSION_INFO])
        if FEATURED_GUEST in tags:
            self._trackPanel().changeFeaturedGuest(tags[FEATURED_GUEST])
        if ISRC in tags:
            self._trackPanel().changeIsrc(tags[ISRC])

    def _saveButton(self):
        return AbstractButtonDriver.findIn(self, QPushButton, named(main.SAVE_BUTTON_NAME))

    def saveTrack(self):
        self._saveButton().click()