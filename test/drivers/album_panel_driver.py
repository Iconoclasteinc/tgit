# -*- coding: utf-8 -*-

import os
from PyQt4.QtGui import QLabel, QLineEdit, QPushButton, QFileDialog

import tgit.ui.album_panel as ui

from test.cute.matchers import named, withBuddy, withPixmapHeight, withPixmapWidth
from test.cute.widgets import (WidgetDriver, LabelDriver, LineEditDriver, AbstractButtonDriver,
                                FileDialogDriver)

# todo use constants from album module
FRONT_COVER_PICTURE = 'frontCoverPicture'
RELEASE_NAME = 'releaseName'
LEAD_PERFORMER = 'leadPerformer'
GUEST_PERFORMERS = 'guestPerformers'
LABEL_NAME = 'labelName'
RECORDING_TIME = 'recordingTime'
RELEASE_TIME = 'releaseTime'
ORIGINAL_RELEASE_TIME = 'originalReleaseTime'
UPC = 'upc'


class AlbumPanelDriver(WidgetDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(AlbumPanelDriver, self).__init__(selector, prober, gesturePerformer)

    def showsMetadata(self, **tags):
        for tag, value in tags.iteritems():
            if tag == RELEASE_NAME:
                self.showsReleaseName(value)
            elif tag == LEAD_PERFORMER:
                self.showsLeadPerformer(value)
            elif tag == GUEST_PERFORMERS:
                self.showsGuestPerformers(value)
            elif tag == LABEL_NAME:
                self.showsLabelName(value)
            elif tag == RECORDING_TIME:
                self.showsRecordingTime(value)
            elif tag == RELEASE_TIME:
                self.showsReleaseTime(value)
            elif tag == ORIGINAL_RELEASE_TIME:
                self.showsOriginalReleaseTime(value)
            elif tag == UPC:
                self.showsUpc(tags[UPC])
            else:
                raise AssertionError("Don't know how to verify <%s>" % tag)

    def changeMetadata(self, **tags):
        for tag, value in tags.iteritems():
            if tag == FRONT_COVER_PICTURE:
                self.changeFrontCoverPicture(value)
            elif tag == RELEASE_NAME:
                self.changeReleaseName(value)
            elif tag == LEAD_PERFORMER:
                self.changeLeadPerformer(value)
            elif tag == GUEST_PERFORMERS:
                self.changeGuestPerformers(value)
            elif tag == LABEL_NAME:
                self.changeLabelName(value)
            elif tag == RECORDING_TIME:
                self.changeRecordingTime(value)
            elif tag == RELEASE_TIME:
                self.changeReleaseTime(value)
            elif tag == ORIGINAL_RELEASE_TIME:
                self.changeOriginalReleaseTime(value)
            elif tag == UPC:
                self.changeUpc(tags[UPC])
            else:
                raise AssertionError("Don't know how to edit <%s>" % tag)

    def displaysFrontCoverPictureWithSize(self, width, height):
        label = LabelDriver.findIn(self, QLabel, named(ui.FRONT_COVER_PICTURE_NAME))
        label.isShowingOnScreen()
        label.hasPixmap(withPixmapHeight(height))
        label.hasPixmap(withPixmapWidth(width))

    def changeFrontCoverPicture(self, filename):
        self._openSelectPictureDialog()
        self._selectPicture(filename)
        self.displaysFrontCoverPictureWithSize(*ui.FRONT_COVER_DISPLAY_SIZE)

    def _openSelectPictureDialog(self):
        button = AbstractButtonDriver.findIn(self, QPushButton, named(ui.SELECT_PICTURE_BUTTON_NAME))
        button.click()

    def _selectPicture(self, filename):
        dialog = FileDialogDriver.findIn(self, QFileDialog, named(ui.SELECT_PICTURE_DIALOG_NAME))
        dialog.navigateToDir(os.path.dirname(filename))
        dialog.selectFile(os.path.basename(filename))
        dialog.accept()

    def showsReleaseName(self, name):
        label = LabelDriver.findIn(self, QLabel, withBuddy(named(ui.RELEASE_NAME_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.RELEASE_NAME_NAME))
        edit.hasText(name)
        
    def changeReleaseName(self, name):
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.RELEASE_NAME_NAME))
        edit.replaceAllText(name)

    def showsLeadPerformer(self, name):
        label = LabelDriver.findIn(self, QLabel, withBuddy(named(ui.LEAD_PERFORMER_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.LEAD_PERFORMER_NAME))
        edit.hasText(name)

    def changeLeadPerformer(self, name):
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.LEAD_PERFORMER_NAME))
        edit.replaceAllText(name)

    def showsGuestPerformers(self, names):
        label = LabelDriver.findIn(self, QLabel, withBuddy(named(ui.GUEST_PERFORMERS_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.GUEST_PERFORMERS_NAME))
        edit.hasText(names)

    def changeGuestPerformers(self, names):
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.GUEST_PERFORMERS_NAME))
        edit.replaceAllText(names)

    def showsLabelName(self, name):
        label = LabelDriver.findIn(self, QLabel, withBuddy(named(ui.LABEL_NAME_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.LABEL_NAME_NAME))
        edit.hasText(name)

    def changeLabelName(self, name):
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.LABEL_NAME_NAME))
        edit.replaceAllText(name)

    def showsRecordingTime(self, time):
        label = LabelDriver.findIn(self, QLabel, withBuddy(named(ui.RECORDING_TIME_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.RECORDING_TIME_NAME))
        edit.hasText(time)

    def changeRecordingTime(self, time):
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.RECORDING_TIME_NAME))
        edit.replaceAllText(time)

    def showsReleaseTime(self, time):
        label = LabelDriver.findIn(self, QLabel, withBuddy(named(ui.RELEASE_TIME_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.RELEASE_TIME_NAME))
        edit.hasText(time)

    def changeReleaseTime(self, time):
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.RELEASE_TIME_NAME))
        edit.replaceAllText(time)

    def showsOriginalReleaseTime(self, time):
        label = LabelDriver.findIn(self, QLabel, withBuddy(named(ui.ORIGINAL_RELEASE_TIME_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.ORIGINAL_RELEASE_TIME_NAME))
        edit.hasText(time)

    def changeOriginalReleaseTime(self, time):
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.ORIGINAL_RELEASE_TIME_NAME))
        edit.replaceAllText(time)

    def showsUpc(self, code):
        label = LabelDriver.findIn(self, QLabel, withBuddy(named(ui.UPC_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.UPC_NAME))
        edit.hasText(code)

    def changeUpc(self, code):
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.UPC_NAME))
        edit.replaceAllText(code)