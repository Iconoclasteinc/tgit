# -*- coding: utf-8 -*-

import os
from PyQt4.Qt import QPushButton, QFileDialog, QWidget
from tests.cute.matchers import named
from tests.cute.widgets import MainWindowDriver, AbstractButtonDriver, FileDialogDriver
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
UPC = 'upc'
RELEASE_DATE = 'releaseDate'
LEAD_PERFORMER = 'leadPerformer'
RELEASE_NAME = 'releaseName'
FRONT_COVER_EMBEDDED_TEXT = 'frontCoverEmbeddedText'
FRONT_COVER_PICTURE = 'frontCoverPicture'


class TaggerDriver(MainWindowDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(TaggerDriver, self).__init__(selector, prober, gesturePerformer)

    def importTrack(self, path):
        self._openImportTrackDialog()
        self._selectTrack(path)

    def _openImportTrackDialog(self):
        button = AbstractButtonDriver.find(self, QPushButton, named(main.ADD_FILE_BUTTON_NAME))
        button.click()

    def _selectTrack(self, trackFile):
        dialog = FileDialogDriver.find(self, QFileDialog, named(main.IMPORT_TRACK_DIALOG_NAME))
        dialog.showHiddenFiles()
        dialog.navigateToDir(os.path.dirname(trackFile))
        dialog.selectFile(os.path.basename(trackFile))
        dialog.accept()
        # todo probe that album panel is shown

    def showsAlbumMetadata(self, **tags):
        if RELEASE_NAME in tags:
            self.albumPanel().showsReleaseName(tags[RELEASE_NAME])
        if LEAD_PERFORMER in tags:
            self.albumPanel().showsLeadPerformer(tags[LEAD_PERFORMER])
        if RELEASE_DATE in tags:
            self.albumPanel().showsReleaseDate(tags[RELEASE_DATE])
        if UPC in tags:
            self.albumPanel().showsUpc(tags[UPC])

    def albumPanel(self):
        return AlbumPanelDriver.find(self, QWidget, named(album.ALBUM_PANEL_NAME))

    def editAlbumMetadata(self, **tags):
        if FRONT_COVER_PICTURE in tags:
            self.albumPanel().changeFrontCoverPicture(tags[FRONT_COVER_PICTURE])
        if RELEASE_NAME in tags:
            self.albumPanel().changeReleaseName(tags[RELEASE_NAME])
        if LEAD_PERFORMER in tags:
            self.albumPanel().changeLeadPerformer(tags[LEAD_PERFORMER])
        if RELEASE_DATE in tags:
            self.albumPanel().changeReleaseDate(tags[RELEASE_DATE])
        if UPC in tags:
            self.albumPanel().changeUpc(tags[UPC])

    def nextStep(self):
        button = AbstractButtonDriver.find(self, QPushButton, named(main.NEXT_STEP_BUTTON_NAME))
        button.click()

    def showsTrackMetadata(self, **tags):
        if TRACK_TITLE in tags:
            self.trackPanel().showsTrackTitle(tags[TRACK_TITLE])
        if VERSION_INFO in tags:
            self.trackPanel().showsVersionInfo(tags[VERSION_INFO])
        if FEATURED_GUEST in tags:
            self.trackPanel().showsFeaturedGuest(tags[FEATURED_GUEST])
        if ISRC in tags:
            self.trackPanel().showsIsrc(tags[ISRC])
        if BITRATE in tags:
            self.trackPanel().showsBitrate(tags[BITRATE])
        if DURATION in tags:
            self.trackPanel().showsDuration(tags[DURATION])

    def trackPanel(self):
        return TrackPanelDriver.find(self, QWidget, named(track.TRACK_PANEL_NAME))

    def editTrackMetadata(self, **tags):
        if TRACK_TITLE in tags:
            self.trackPanel().changeTrackTitle(tags[TRACK_TITLE])
        if VERSION_INFO in tags:
            self.trackPanel().changeVersionInfo(tags[VERSION_INFO])
        if FEATURED_GUEST in tags:
            self.trackPanel().changeFeaturedGuest(tags[FEATURED_GUEST])
        if ISRC in tags:
            self.trackPanel().changeIsrc(tags[ISRC])

    def saveTrack(self):
        button = AbstractButtonDriver.find(self, QPushButton, named(main.SAVE_BUTTON_NAME))
        button.click()