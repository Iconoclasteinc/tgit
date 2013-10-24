# -*- coding: utf-8 -*-

import os

from PyQt4.QtGui import QLabel, QLineEdit, QPushButton, QFileDialog

from test.cute.matchers import named, withBuddy, withPixmapHeight, withPixmapWidth
from test.cute.widgets import (dialogWindow, WidgetDriver, LabelDriver, LineEditDriver,
                               AbstractButtonDriver,
                               FileDialogDriver)

import tgit.album as album
from tgit.ui import constants as ui


class AlbumPageDriver(WidgetDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(AlbumPageDriver, self).__init__(selector, prober, gesturePerformer)

    def showsMetadata(self, **tags):
        for tag, value in tags.iteritems():
            if tag == album.TITLE:
                self.showsReleaseName(value)
            elif tag == album.LEAD_PERFORMER:
                self.showsLeadPerformer(value)
            elif tag == album.GUEST_PERFORMERS:
                self.showsGuestPerformers(value)
            elif tag == album.LABEL_NAME:
                self.showsLabelName(value)
            elif tag == album.RECORDING_TIME:
                self.showsRecordingTime(value)
            elif tag == album.RELEASE_TIME:
                self.showsReleaseTime(value)
            elif tag == album.ORIGINAL_RELEASE_TIME:
                self.showsOriginalReleaseTime(value)
            elif tag == album.UPC:
                self.showsUpc(value)
            else:
                raise AssertionError("Don't know how to verify '%s'" % tag)

    def changeMetadata(self, **tags):
        for tag, value in tags.iteritems():
            if tag == album.FRONT_COVER:
                self.chooseFrontCoverPicture(value)
            elif tag == album.TITLE:
                self.changeReleaseName(value)
            elif tag == album.LEAD_PERFORMER:
                self.changeLeadPerformer(value)
            elif tag == album.GUEST_PERFORMERS:
                self.changeGuestPerformers(value)
            elif tag == album.LABEL_NAME:
                self.changeLabelName(value)
            elif tag == album.RECORDING_TIME:
                self.changeRecordingTime(value)
            elif tag == album.RELEASE_TIME:
                self.changeReleaseTime(value)
            elif tag == album.ORIGINAL_RELEASE_TIME:
                self.changeOriginalReleaseTime(value)
            elif tag == album.UPC:
                self.changeUpc(value)
            else:
                raise AssertionError("Don't know how to edit '%s'" % tag)

    def displaysFrontCoverPictureWithSize(self, width, height):
        label = LabelDriver.findSingle(self, QLabel, named(ui.FRONT_COVER_PIXMAP_NAME))
        label.isShowingOnScreen()
        label.hasPixmap(withPixmapHeight(height))
        label.hasPixmap(withPixmapWidth(width))

    def chooseFrontCoverPicture(self, filename):
        self.selectFrontCover()
        self._chooseImageFile(filename)
        self.displaysFrontCoverPictureWithSize(*ui.FRONT_COVER_PIXMAP_SIZE)

    def selectFrontCover(self):
        button = AbstractButtonDriver.findSingle(self, QPushButton,
                                                 named(ui.SELECT_PICTURE_BUTTON_NAME))
        button.click()

    def _chooseImageFile(self, filename):
        dialog = FileDialogDriver(dialogWindow(QFileDialog,
                                               named(ui.CHOOSE_IMAGE_FILE_DIALOG_NAME)),
                                  self.prober, self.gesturePerformer)
        dialog.navigateToDir(os.path.dirname(filename))
        dialog.selectFile(os.path.basename(filename))
        dialog.accept()

    def showsReleaseName(self, name):
        label = LabelDriver.findSingle(self, QLabel, withBuddy(named(ui.RELEASE_NAME_EDIT_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.RELEASE_NAME_EDIT_NAME))
        edit.hasText(name)
        
    def changeReleaseName(self, name):
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.RELEASE_NAME_EDIT_NAME))
        edit.replaceAllText(name)

    def showsLeadPerformer(self, name):
        label = LabelDriver.findSingle(self, QLabel, withBuddy(named(ui.LEAD_PERFORMER_EDIT_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.LEAD_PERFORMER_EDIT_NAME))
        edit.hasText(name)

    def changeLeadPerformer(self, name):
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.LEAD_PERFORMER_EDIT_NAME))
        edit.replaceAllText(name)

    def showsGuestPerformers(self, names):
        label = LabelDriver.findSingle(self, QLabel,
                                       withBuddy(named(ui.GUEST_PERFORMERS_EDIT_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.GUEST_PERFORMERS_EDIT_NAME))
        edit.hasText(names)

    def changeGuestPerformers(self, names):
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.GUEST_PERFORMERS_EDIT_NAME))
        edit.replaceAllText(names)

    def showsLabelName(self, name):
        label = LabelDriver.findSingle(self, QLabel, withBuddy(named(ui.LABEL_NAME_EDIT_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.LABEL_NAME_EDIT_NAME))
        edit.hasText(name)

    def changeLabelName(self, name):
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.LABEL_NAME_EDIT_NAME))
        edit.replaceAllText(name)

    def showsRecordingTime(self, time):
        label = LabelDriver.findSingle(self, QLabel, withBuddy(named(ui.RECORDING_TIME_EDIT_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.RECORDING_TIME_EDIT_NAME))
        edit.hasText(time)

    def changeRecordingTime(self, time):
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.RECORDING_TIME_EDIT_NAME))
        edit.replaceAllText(time)

    def showsReleaseTime(self, time):
        label = LabelDriver.findSingle(self, QLabel, withBuddy(named(ui.RELEASE_TIME_EDIT_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.RELEASE_TIME_EDIT_NAME))
        edit.hasText(time)

    def changeReleaseTime(self, time):
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.RELEASE_TIME_EDIT_NAME))
        edit.replaceAllText(time)

    def showsOriginalReleaseTime(self, time):
        label = LabelDriver.findSingle(self, QLabel,
                                       withBuddy(named(ui.ORIGINAL_RELEASE_TIME_EDIT_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit,
                                         named(ui.ORIGINAL_RELEASE_TIME_EDIT_NAME))
        edit.hasText(time)

    def changeOriginalReleaseTime(self, time):
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.ORIGINAL_RELEASE_TIME_EDIT_NAME))
        edit.replaceAllText(time)

    def showsUpc(self, code):
        label = LabelDriver.findSingle(self, QLabel, withBuddy(named(ui.UPC_EDIT_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.UPC_EDIT_NAME))
        edit.hasText(code)

    def changeUpc(self, code):
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.UPC_EDIT_NAME))
        edit.replaceAllText(code)