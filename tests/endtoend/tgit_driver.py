# -*- coding: utf-8 -*-

import os
from PyQt4.Qt import QPushButton, QLineEdit, QFileDialog, QLabel
from hamcrest.core import all_of
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
ORIGINAL_RELEASE_DATE = 'originalReleaseDate'
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
        releaseNameLabel = LabelDriver.find(self, QLabel, withBuddy(named(main.RELEASE_NAME_NAME)))
        releaseNameLabel.isShowingOnScreen()
        self._releaseName().hasText(releaseName)

    def displaysFrontCoverPictureWithSize(self, width, height):
        frontCoverImage = LabelDriver.find(self, QLabel, named(main.FRONT_COVER_PICTURE_NAME))
        frontCoverImage.isShowingOnScreen()
        frontCoverImage.hasPixmap(withPixmapHeight(height))
        frontCoverImage.hasPixmap(withPixmapWidth(width))

    def showsMetadata(self, tags):
        self._frontCoverEmbeddedText().hasText(tags[FRONT_COVER_EMBEDDED_TEXT])
        self.showsReleaseName(tags[RELEASE_NAME])
        self._leadPerformer().hasText(tags[LEAD_PERFORMER])
        self._originalReleaseDate().hasText(tags[ORIGINAL_RELEASE_DATE])
        self._upc().hasText(tags[UPC])
        self._trackTitle().hasText(tags[TRACK_TITLE])
        self._featuredGuest().hasText(tags[FEATURED_GUEST])
        self._versionInfo().hasText(tags[VERSION_INFO])
        self._isrc().hasText(tags[ISRC])
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
        self._originalReleaseDate().replaceAllText(tags[ORIGINAL_RELEASE_DATE])
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

    def _originalReleaseDate(self):
        return LineEditDriver.find(self, QLineEdit, named(main.ORIGINAL_RELEASE_DATE_NAME))

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
