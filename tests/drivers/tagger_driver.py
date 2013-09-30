# -*- coding: utf-8 -*-

import os
from PyQt4.Qt import QPushButton, QFileDialog, QWidget, QLabel
from tests.cute.matchers import named, withLabelText
from tests.cute.widgets import (MainWindowDriver, AbstractButtonDriver, FileDialogDriver,
                                WidgetDriver, LabelDriver)
from tests.drivers.album_panel_driver import AlbumPanelDriver
from tests.drivers.track_panel_driver import TrackPanelDriver

import tgit.ui.main_window as main
import tgit.ui.album_panel as album
import tgit.ui.track_panel as track

DURATION = 'duration'
BITRATE = 'bitrate'
ISRC = 'isrc'
VERSION_INFO = 'versionInfo'
FEATURED_GUEST = 'featuredGuest'
TRACK_TITLE = 'trackTitle'


# todo introduce support classes to capture common user workflows
class TaggerDriver(MainWindowDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(TaggerDriver, self).__init__(selector, prober, gesturePerformer)

    def importTrack(self, path):
        self._openImportTrackDialog()
        self._selectTrack(path)
        self._isShowingAlbumManagementPanel()

    def _openImportTrackDialog(self):
        button = AbstractButtonDriver.find(self, QPushButton, named(main.ADD_FILE_BUTTON_NAME))
        button.click()

    def _selectTrack(self, trackFile):
        dialog = FileDialogDriver.find(self, QFileDialog, named(main.IMPORT_TRACK_DIALOG_NAME))
        dialog.showHiddenFiles()
        dialog.navigateToDir(os.path.dirname(trackFile))
        dialog.selectFile(os.path.basename(trackFile))
        dialog.accept()

    def _isShowingAlbumManagementPanel(self):
        self._albumManagementPanel().isShowingOnScreen()
        self._nextStepButton().isEnabled()
        self._previousStepButton().isDisabled()

    def _albumManagementPanel(self):
        return WidgetDriver.find(self, QWidget, named('Album Management Panel'))

    def showsAlbumContains(self, track):
        albumContent = self._albumManagementPanel()
        LabelDriver.find(albumContent, QLabel, withLabelText(track.trackTitle))

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

    def _albumPanel(self):
        return AlbumPanelDriver.find(self, QWidget, named(album.ALBUM_PANEL_NAME))

    def editAlbumMetadata(self, **tags):
        self._albumPanel().changeMetadata(**tags)

    def _nextStepButton(self):
        return AbstractButtonDriver.find(self, QPushButton, named(main.NEXT_STEP_BUTTON_NAME))

    def _previousStepButton(self):
        return AbstractButtonDriver.find(self, QPushButton, named(main.PREVIOUS_STEP_BUTTON_NAME))

    def backToAlbumMetadata(self):
        self._previousStepButton().click()
        self._trackPanel().isHidden()
        self._isShowingAlbumMetadataPanel()

    def showsTrackMetadata(self, **tags):
        self.navigateToTrackMetadata()
        self._trackPanel().showsMetadata(**tags)

    def _isShowingTrackMetadataPanel(self):
        self._previousStepButton().isEnabled()
        self._nextStepButton().isDisabled()
        self._trackPanel().isShowingOnScreen()

    def navigateToTrackMetadata(self):
        self._nextStepButton().click()
        self._albumPanel().isHidden()
        self._isShowingTrackMetadataPanel()

    def _trackPanel(self):
        return TrackPanelDriver.find(self, QWidget, named(track.TRACK_PANEL_NAME))

    def editTrackMetadata(self, **tags):
        if TRACK_TITLE in tags:
            self._trackPanel().changeTrackTitle(tags[TRACK_TITLE])
        if VERSION_INFO in tags:
            self._trackPanel().changeVersionInfo(tags[VERSION_INFO])
        if FEATURED_GUEST in tags:
            self._trackPanel().changeFeaturedGuest(tags[FEATURED_GUEST])
        if ISRC in tags:
            self._trackPanel().changeIsrc(tags[ISRC])

    def saveTrack(self):
        button = AbstractButtonDriver.find(self, QPushButton, named(main.SAVE_BUTTON_NAME))
        button.click()