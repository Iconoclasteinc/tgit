# -*- coding: utf-8 -*-

import os
from PyQt4.Qt import QPushButton, QLineEdit, QFileDialog, QLabel, QWidget
from tests.cute.prober import EventProcessingProber
from tests.cute.matchers import (named, withBuddy, showingOnScreen, withPixmapHeight,
                                 withPixmapWidth)
from tests.cute.widgets import mainWindow
from tests.cute.widgets import (MainWindowDriver, AbstractButtonDriver, LineEditDriver, LabelDriver,
                                FileDialogDriver)
from tests.cute.robot import Robot
from tests.drivers.album_panel_driver import AlbumPanelDriver

import tgit.ui.main_window as main
import tgit.ui.album_panel as album

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
    def __init__(self, timeoutInMs):
        super(TaggerDriver, self).__init__(
            mainWindow(named(main.MAIN_WINDOW_NAME), showingOnScreen()),
            EventProcessingProber(timeoutInMs=timeoutInMs),
            Robot())

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
            self.showsReleaseName(tags[RELEASE_NAME])
        if LEAD_PERFORMER in tags:
            self.showsLeadPerformer(tags[LEAD_PERFORMER])
        if RELEASE_DATE in tags:
            self.showsReleaseDate(tags[RELEASE_DATE])
        if UPC in tags:
            self.showsUpc(tags[UPC])

    def showsReleaseName(self, name):
        self._albumPanelDriver().showsReleaseName(name)

    def _albumPanelDriver(self):
        return AlbumPanelDriver.find(self, QWidget, named(album.ALBUM_PANEL_NAME))

    def showsLeadPerformer(self, name):
        self._albumPanelDriver().showsLeadPerformer(name)

    def showsReleaseDate(self, date):
        self._albumPanelDriver().showsReleaseDate(date)

    def showsUpc(self, code):
        self._albumPanelDriver().showsUpc(code)

    def showsTrackTitle(self, trackTitle):
        label = LabelDriver.find(self, QLabel, withBuddy(named(main.TRACK_TITLE_NAME)))
        label.isShowingOnScreen()
        self._trackTitleEdit().hasText(trackTitle)

    def showsVersionInfo(self, versionInfo):
        label = LabelDriver.find(self, QLabel, withBuddy(named(main.VERSION_INFO_NAME)))
        label.isShowingOnScreen()
        self._versionInfoEdit().hasText(versionInfo)

    def showsFeaturedGuest(self, featuredGuest):
        label = LabelDriver.find(self, QLabel, withBuddy(named(main.VERSION_INFO_NAME)))
        label.isShowingOnScreen()
        self._featuredGuestEdit().hasText(featuredGuest)

    def showsIsrc(self, isrc):
        label = LabelDriver.find(self, QLabel, withBuddy(named(main.ISRC_NAME)))
        label.isShowingOnScreen()
        self._isrcEdit().hasText(isrc)

    def showsBitrate(self, bitrate):
        label = LabelDriver.find(self, QLabel, withBuddy(named(main.BITRATE_NAME)))
        label.isShowingOnScreen()
        self._bitrateLabel().hasText(bitrate)

    def showsDuration(self, duration):
        label = LabelDriver.find(self, QLabel, withBuddy(named(main.DURATION_NAME)))
        label.isShowingOnScreen()
        self._durationLabel().hasText(duration)

    def editAlbumMetadata(self, **tags):
        if FRONT_COVER_PICTURE in tags:
            self.changeFrontCoverPicture(tags[FRONT_COVER_PICTURE])
        if RELEASE_NAME in tags:
            self.changeReleaseName(tags[RELEASE_NAME])
        if LEAD_PERFORMER in tags:
            self.changeLeadPerformer(tags[LEAD_PERFORMER])
        if RELEASE_DATE in tags:
            self.changeReleaseDate(tags[RELEASE_DATE])
        if UPC in tags:
            self.changeUpc(tags[UPC])

    def nextStep(self):
        button = AbstractButtonDriver.find(self, QPushButton, named(main.NEXT_STEP_BUTTON_NAME))
        button.click()

    def showsTrackMetadata(self, **tags):
        if TRACK_TITLE in tags:
            self.showsTrackTitle(tags[TRACK_TITLE])
        if VERSION_INFO in tags:
            self.showsVersionInfo(tags[VERSION_INFO])
        if FEATURED_GUEST in tags:
            self.showsFeaturedGuest(tags[FEATURED_GUEST])
        if ISRC in tags:
            self.showsIsrc(tags[ISRC])
        if BITRATE in tags:
            self.showsBitrate(tags[BITRATE])
        if DURATION in tags:
            self.showsDuration(tags[DURATION])

    def editTrackMetadata(self, **tags):
        if TRACK_TITLE in tags:
            self.changeTrackTitle(tags[TRACK_TITLE])
        if VERSION_INFO in tags:
            self.changeVersionInfo(tags[VERSION_INFO])
        if FEATURED_GUEST in tags:
            self.changeFeaturedGuest(tags[FEATURED_GUEST])
        if ISRC in tags:
            self.changeIsrc(tags[ISRC])

    def changeFrontCoverPicture(self, filename):
        self._albumPanelDriver().changeFrontCoverPicture(filename)

    def changeReleaseName(self, name):
        self._albumPanelDriver().changeReleaseName(name)

    def changeLeadPerformer(self, name):
        self._albumPanelDriver().changeLeadPerformer(name)

    def changeReleaseDate(self, date):
        self._albumPanelDriver().changeReleaseDate(date)

    def changeUpc(self, code):
        self._albumPanelDriver().changeUpc(code)

    def changeTrackTitle(self, title):
        self._trackTitleEdit().replaceAllText(title)

    def changeVersionInfo(self, info):
        self._versionInfoEdit().replaceAllText(info)

    def changeFeaturedGuest(self, name):
        self._featuredGuestEdit().replaceAllText(name)

    def changeIsrc(self, code):
        self._isrcEdit().replaceAllText(code)

    def saveTrack(self):
        button = AbstractButtonDriver.find(self, QPushButton, named(main.SAVE_BUTTON_NAME))
        button.click()

    def _trackTitleEdit(self):
        return LineEditDriver.find(self, QLineEdit, named(main.TRACK_TITLE_NAME))

    def _versionInfoEdit(self):
        return LineEditDriver.find(self, QLineEdit, named(main.VERSION_INFO_NAME))

    def _featuredGuestEdit(self):
        return LineEditDriver.find(self, QLineEdit, named(main.FEATURED_GUEST_NAME))

    def _isrcEdit(self):
        return LineEditDriver.find(self, QLineEdit, named(main.ISRC_NAME))

    def _bitrateLabel(self):
        return LabelDriver.find(self, QLabel, named(main.BITRATE_NAME))

    def _durationLabel(self):
        return LabelDriver.find(self, QLabel, named(main.DURATION_NAME))
