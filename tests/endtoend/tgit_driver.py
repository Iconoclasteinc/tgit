# -*- coding: utf-8 -*-

import os
from PyQt4.Qt import QPushButton, QLineEdit, QFileDialog, QLabel
from tests.cute.prober import EventProcessingProber
from tests.cute.matchers import (named, withBuddy, showingOnScreen, withPixmapHeight,
                                 withPixmapWidth)
from tests.cute.widgets import mainWindow
from tests.cute.widgets import (MainWindowDriver, AbstractButtonDriver, LineEditDriver, LabelDriver,
                                FileDialogDriver)
from tests.cute.robot import Robot

import tgit.ui.main_window as main

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


class TGiTDriver(MainWindowDriver):
    def __init__(self, timeout_in_ms):
        super(TGiTDriver, self).__init__(
            mainWindow(named(main.MAIN_WINDOW_NAME), showingOnScreen()),
            EventProcessingProber(timeoutInMs=timeout_in_ms),
            Robot())

    def importTrack(self, path):
        self._openImportTrackDialog()
        self._selectTrack(path)

    def showsReleaseName(self, releaseName):
        label = LabelDriver.find(self, QLabel, withBuddy(named(main.RELEASE_NAME_NAME)))
        label.isShowingOnScreen()
        self._releaseName().hasText(releaseName)

    def displaysFrontCoverPictureWithSize(self, width, height):
        label = LabelDriver.find(self, QLabel, named(main.FRONT_COVER_PICTURE_NAME))
        label.isShowingOnScreen()
        label.hasPixmap(withPixmapHeight(height))
        label.hasPixmap(withPixmapWidth(width))

    def showsLeadPerformer(self, leadPerformer):
        label = LabelDriver.find(self, QLabel, withBuddy(named(main.LEAD_PERFORMER_NAME)))
        label.isShowingOnScreen()
        self._leadPerformer().hasText(leadPerformer)

    def showsReleaseDate(self, releaseDate):
        label = LabelDriver.find(self, QLabel, withBuddy(named(main.RELEASE_DATE_NAME)))
        label.isShowingOnScreen()
        self._releaseDate().hasText(releaseDate)

    def showsUpc(self, upc):
        label = LabelDriver.find(self, QLabel, withBuddy(named(main.UPC_NAME)))
        label.isShowingOnScreen()
        self._upc().hasText(upc)

    def showsTrackTitle(self, trackTitle):
        label = LabelDriver.find(self, QLabel, withBuddy(named(main.TRACK_TITLE_NAME)))
        label.isShowingOnScreen()
        self._trackTitle().hasText(trackTitle)

    def showsVersionInfo(self, versionInfo):
        label = LabelDriver.find(self, QLabel, withBuddy(named(main.VERSION_INFO_NAME)))
        label.isShowingOnScreen()
        self._versionInfo().hasText(versionInfo)

    def showsFeaturedGuest(self, featuredGuest):
        label = LabelDriver.find(self, QLabel, withBuddy(named(main.VERSION_INFO_NAME)))
        label.isShowingOnScreen()
        self._featuredGuest().hasText(featuredGuest)

    def showsIsrc(self, isrc):
        label = LabelDriver.find(self, QLabel, withBuddy(named(main.ISRC_NAME)))
        label.isShowingOnScreen()
        self._isrc().hasText(isrc)

    def showsMetadata(self, tags):
        self._frontCoverEmbeddedText().hasText(tags[FRONT_COVER_EMBEDDED_TEXT])
        self.showsReleaseName(tags[RELEASE_NAME])
        self.showsLeadPerformer(tags[LEAD_PERFORMER])
        self.showsReleaseDate(tags[RELEASE_DATE])
        self.showsUpc(tags[UPC])
        self.showsTrackTitle(tags[TRACK_TITLE])
        self.showsVersionInfo(tags[VERSION_INFO])
        self.showsFeaturedGuest(tags[FEATURED_GUEST])
        self.showsIsrc(tags[ISRC])
        self._bitrate().hasText(tags[BITRATE])
        self._trackDuration().hasText(tags[DURATION])

    def _openImportTrackDialog(self):
        addFileButton = AbstractButtonDriver.find(self, QPushButton,
                                                  named(main.ADD_FILE_BUTTON_NAME))
        addFileButton.click()

    def _selectTrack(self, trackFile):
        dialog = self._addFileDialog()
        dialog.showHiddenFiles()
        dialog.navigateToDir(os.path.dirname(trackFile))
        dialog.selectFile(os.path.basename(trackFile))
        dialog.accept()

    def _addFileDialog(self):
        return FileDialogDriver.find(self, QFileDialog, named(main.IMPORT_TRACK_DIALOG_NAME))

    def editMetadata(self, tags):
        self._loadPicture(tags[FRONT_COVER_PICTURE])
        self._releaseName().replaceAllText(tags[RELEASE_NAME])
        self._leadPerformer().replaceAllText(tags[LEAD_PERFORMER])
        self._releaseDate().replaceAllText(tags[RELEASE_DATE])
        self._upc().replaceAllText(tags[UPC])
        self._trackTitle().replaceAllText(tags[TRACK_TITLE])
        self._versionInfo().replaceAllText(tags[VERSION_INFO])
        self._featuredGuest().replaceAllText(tags[FEATURED_GUEST])
        self._isrc().replaceAllText(tags[ISRC])

    def _loadPicture(self, pictureFile):
        self._openSelectPictureDialog()
        self._selectPicture(pictureFile)

    def _openSelectPictureDialog(self):
        selectPictureButton = AbstractButtonDriver.find(self, QPushButton,
                                                        named(main.SELECT_PICTURE_BUTTON_NAME))
        selectPictureButton.click()

    def _selectPicture(self, pictureFile):
        selectPictureDialog = self._selectPictureDialog()
        selectPictureDialog.navigateToDir(os.path.dirname(pictureFile))
        selectPictureDialog.selectFile(os.path.basename(pictureFile))
        selectPictureDialog.accept()

    def _selectPictureDialog(self):
        return FileDialogDriver.find(self, QFileDialog, named(main.SELECT_PICTURE_DIALOG_NAME))

    def saveAudioFile(self):
        saveButton = AbstractButtonDriver.find(self, QPushButton, named(main.SAVE_BUTTON_NAME))
        saveButton.click()

    def _frontCoverEmbeddedText(self):
        return LabelDriver.find(self, QLabel, named(main.FRONT_COVER_EMBEDDED_TEXT_NAME))

    def _releaseName(self):
        return LineEditDriver.find(self, QLineEdit, named(main.RELEASE_NAME_NAME))

    def _leadPerformer(self):
        return LineEditDriver.find(self, QLineEdit, named(main.LEAD_PERFORMER_NAME))

    def _releaseDate(self):
        return LineEditDriver.find(self, QLineEdit, named(main.RELEASE_DATE_NAME))

    def _upc(self):
        return LineEditDriver.find(self, QLineEdit, named(main.UPC_NAME))

    def _trackTitle(self):
        return LineEditDriver.find(self, QLineEdit, named(main.TRACK_TITLE_NAME))

    def _versionInfo(self):
        return LineEditDriver.find(self, QLineEdit, named(main.VERSION_INFO_NAME))

    def _featuredGuest(self):
        return LineEditDriver.find(self, QLineEdit, named(main.FEATURED_GUEST_NAME))

    def _isrc(self):
        return LineEditDriver.find(self, QLineEdit, named(main.ISRC_NAME))

    def _bitrate(self):
        return LabelDriver.find(self, QLabel, named(main.BITRATE_NAME))

    def _trackDuration(self):
        return LabelDriver.find(self, QLabel, named(main.DURATION_NAME))
