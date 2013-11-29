# -*- coding: utf-8 -*-

import os

from PyQt4.QtGui import QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit

from test.cute.matchers import named, withBuddy, withPixmapHeight, withPixmapWidth
from test.cute.widgets import (window, WidgetDriver, LabelDriver, LineEditDriver,
                               ButtonDriver, FileDialogDriver, TextEditDriver)

import tgit.tags as tags
from tgit.ui import AlbumPage


class AlbumPageDriver(WidgetDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(AlbumPageDriver, self).__init__(selector, prober, gesturePerformer)

    def showsMetadata(self, **meta):
        for tag, value in meta.iteritems():
            if tag == tags.RELEASE_NAME:
                self.showsReleaseName(value)
            elif tag == tags.LEAD_PERFORMER:
                self.showsLeadPerformer(value)
            elif tag == tags.GUEST_PERFORMERS:
                self.showsGuestPerformers(value)
            elif tag == tags.LABEL_NAME:
                self.showsLabelName(value)
            elif tag == tags.CATALOG_NUMBER:
                self.showsCatalogNumber(value)
            elif tag == tags.UPC:
                self.showsUpc(value)
            elif tag == tags.RECORDING_TIME:
                self.showsRecordingTime(value)
            elif tag == tags.RELEASE_TIME:
                self.showsReleaseTime(value)
            elif tag == tags.ORIGINAL_RELEASE_TIME:
                self.showsOriginalReleaseTime(value)
            elif tag == tags.RECORDING_STUDIOS:
                self.showsRecordingStudios(value)
            elif tag == tags.PRODUCER:
                self.showsProducer(value)
            elif tag == tags.MIXER:
                self.showsMixer(value)
            else:
                raise AssertionError("Don't know how to verify '%s'" % tag)

    def changeMetadata(self, **meta):
        for tag, value in meta.iteritems():
            if tag == tags.FRONT_COVER:
                self.chooseFrontCoverPicture(value)
            elif tag == tags.RELEASE_NAME:
                self.changeReleaseName(value)
            elif tag == tags.LEAD_PERFORMER:
                self.changeLeadPerformer(value)
            elif tag == tags.GUEST_PERFORMERS:
                self.changeGuestPerformers(value)
            elif tag == tags.LABEL_NAME:
                self.changeLabelName(value)
            elif tag == tags.CATALOG_NUMBER:
                self.changeCatalogNumber(value)
            elif tag == tags.UPC:
                self.changeUpc(value)
            elif tag == tags.RECORDING_TIME:
                self.changeRecordingTime(value)
            elif tag == tags.RELEASE_TIME:
                self.changeReleaseTime(value)
            elif tag == tags.ORIGINAL_RELEASE_TIME:
                self.changeOriginalReleaseTime(value)
            elif tag == tags.RECORDING_STUDIOS:
                self.changeRecordingStudios(value)
            elif tag == tags.PRODUCER:
                self.changeProducer(value)
            elif tag == tags.MIXER:
                self.changeMixer(value)
            else:
                raise AssertionError("Don't know how to edit '%s'" % tag)

    def displaysFrontCoverPictureWithSize(self, width, height):
        label = LabelDriver.findSingle(self, QLabel, named(AlbumPage.FRONT_COVER_FIELD_NAME))
        label.isShowingOnScreen()
        label.hasPixmap(withPixmapHeight(height))
        label.hasPixmap(withPixmapWidth(width))

    def chooseFrontCoverPicture(self, filename):
        self.selectFrontCover()
        self._chooseImageFile(filename)
        self.displaysFrontCoverPictureWithSize(*AlbumPage.FRONT_COVER_SIZE)

    def selectFrontCover(self):
        button = ButtonDriver.findSingle(self, QPushButton,
                                         named(AlbumPage.SELECT_PICTURE_BUTTON_NAME))
        button.click()

    def _chooseImageFile(self, filename):
        dialog = FileDialogDriver(
            window(QFileDialog, named(AlbumPage.CHOOSE_IMAGE_FILE_DIALOG_NAME)),
            self.prober, self.gesturePerformer)
        dialog.navigateToDir(os.path.dirname(filename))
        dialog.selectFile(os.path.basename(filename))
        dialog.accept()

    def showsReleaseName(self, name):
        label = LabelDriver.findSingle(self, QLabel,
                                       withBuddy(named(AlbumPage.RELEASE_NAME_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit, named(AlbumPage.RELEASE_NAME_FIELD_NAME))
        edit.hasText(name)

    def changeReleaseName(self, name):
        edit = LineEditDriver.findSingle(self, QLineEdit, named(AlbumPage.RELEASE_NAME_FIELD_NAME))
        edit.changeText(name)

    def showsLeadPerformer(self, name):
        label = LabelDriver.findSingle(self, QLabel,
                                       withBuddy(named(AlbumPage.LEAD_PERFORMER_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit,
                                         named(AlbumPage.LEAD_PERFORMER_FIELD_NAME))
        edit.hasText(name)

    def changeLeadPerformer(self, name):
        edit = LineEditDriver.findSingle(self, QLineEdit,
                                         named(AlbumPage.LEAD_PERFORMER_FIELD_NAME))
        edit.changeText(name)

    def showsGuestPerformers(self, names):
        label = LabelDriver.findSingle(self, QLabel,
                                       withBuddy(named(AlbumPage.GUEST_PERFORMERS_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit,
                                         named(AlbumPage.GUEST_PERFORMERS_FIELD_NAME))
        edit.hasText(names)

    def changeGuestPerformers(self, names):
        edit = LineEditDriver.findSingle(self, QLineEdit,
                                         named(AlbumPage.GUEST_PERFORMERS_FIELD_NAME))
        edit.changeText(names)

    def showsLabelName(self, name):
        label = LabelDriver.findSingle(self, QLabel,
                                       withBuddy(named(AlbumPage.LABEL_NAME_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit, named(AlbumPage.LABEL_NAME_FIELD_NAME))
        edit.hasText(name)

    def changeLabelName(self, name):
        edit = LineEditDriver.findSingle(self, QLineEdit, named(AlbumPage.LABEL_NAME_FIELD_NAME))
        edit.changeText(name)

    def showsLabelTown(self, town):
        # todo I'd rather have label = self.labelWithBuddy(named(AlbumPage.LABEL_TOWN))
        label = LabelDriver.findSingle(self, QLabel,
                                       withBuddy(named(AlbumPage.LABEL_TOWN_FIELD_NAME)))
        label.isShowingOnScreen()
        # todo I'd rather have lineEdit = self.lineEdit(named(AlbumPage.LABEL_TOWN))
        edit = LineEditDriver.findSingle(self, QLineEdit, named(AlbumPage.LABEL_TOWN_FIELD_NAME))
        edit.isDisabled()
        edit.hasText(town)

    def showsArea(self, area):
        label = LabelDriver.findSingle(self, QLabel, withBuddy(named(AlbumPage.AREA_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit, named(AlbumPage.AREA_FIELD_NAME))
        edit.isDisabled()
        edit.hasText(area)

    def showsCatalogNumber(self, number):
        label = LabelDriver.findSingle(self, QLabel,
                                       withBuddy(named(AlbumPage.CATALOG_NUMBER_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit,
                                         named(AlbumPage.CATALOG_NUMBER_FIELD_NAME))
        edit.hasText(number)

    def changeCatalogNumber(self, number):
        edit = LineEditDriver.findSingle(self, QLineEdit,
                                         named(AlbumPage.CATALOG_NUMBER_FIELD_NAME))
        edit.changeText(number)

    def showsUpc(self, code):
        label = LabelDriver.findSingle(self, QLabel, withBuddy(named(AlbumPage.UPC_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit, named(AlbumPage.UPC_FIELD_NAME))
        edit.hasText(code)

    def changeUpc(self, code):
        edit = LineEditDriver.findSingle(self, QLineEdit, named(AlbumPage.UPC_FIELD_NAME))
        edit.changeText(code)

    def showsRecordingTime(self, time):
        label = LabelDriver.findSingle(self, QLabel,
                                       withBuddy(named(AlbumPage.RECORDING_TIME_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit,
                                         named(AlbumPage.RECORDING_TIME_FIELD_NAME))
        edit.hasText(time)

    def changeRecordingTime(self, time):
        edit = LineEditDriver.findSingle(self, QLineEdit,
                                         named(AlbumPage.RECORDING_TIME_FIELD_NAME))
        edit.changeText(time)

    def showsReleaseTime(self, time):
        label = LabelDriver.findSingle(self, QLabel,
                                       withBuddy(named(AlbumPage.RELEASE_TIME_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit, named(AlbumPage.RELEASE_TIME_FIELD_NAME))
        edit.hasText(time)

    def changeReleaseTime(self, time):
        edit = LineEditDriver.findSingle(self, QLineEdit, named(AlbumPage.RELEASE_TIME_FIELD_NAME))
        edit.changeText(time)

    def showsDigitalReleaseTime(self, time):
        label = LabelDriver.findSingle(self, QLabel,
                                       withBuddy(named(AlbumPage.DIGITAL_RELEASE_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit,
                                         named(AlbumPage.DIGITAL_RELEASE_FIELD_NAME))
        edit.isDisabled()
        edit.hasText(time)

    def showsOriginalReleaseTime(self, time):
        label = LabelDriver.findSingle(self, QLabel,
                                       withBuddy(named(AlbumPage.ORIGINAL_RELEASE_TIME_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit,
                                         named(AlbumPage.ORIGINAL_RELEASE_TIME_FIELD_NAME))
        edit.hasText(time)

    def changeOriginalReleaseTime(self, time):
        edit = LineEditDriver.findSingle(self, QLineEdit,
                                         named(AlbumPage.ORIGINAL_RELEASE_TIME_FIELD_NAME))
        edit.changeText(time)

    def showsRecordingStudios(self, studios):
        label = LabelDriver.findSingle(self, QLabel,
                                       withBuddy(named(AlbumPage.RECORDING_STUDIOS_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit,
                                         named(AlbumPage.RECORDING_STUDIOS_FIELD_NAME))
        edit.hasText(studios)

    def changeRecordingStudios(self, studios):
        edit = LineEditDriver.findSingle(self, QLineEdit,
                                         named(AlbumPage.RECORDING_STUDIOS_FIELD_NAME))
        edit.changeText(studios)

    def showsProducer(self, producer):
        label = LabelDriver.findSingle(self, QLabel,
                                       withBuddy(named(AlbumPage.PRODUCER_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit, named(AlbumPage.PRODUCER_FIELD_NAME))
        edit.hasText(producer)

    def changeProducer(self, producer):
        edit = LineEditDriver.findSingle(self, QLineEdit, named(AlbumPage.PRODUCER_FIELD_NAME))
        edit.changeText(producer)

    def showsMixer(self, mixer):
        label = LabelDriver.findSingle(self, QLabel, withBuddy(named(AlbumPage.MIXER_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit, named(AlbumPage.MIXER_FIELD_NAME))
        edit.hasText(mixer)

    def changeMixer(self, mixer):
        edit = LineEditDriver.findSingle(self, QLineEdit, named(AlbumPage.MIXER_FIELD_NAME))
        edit.changeText(mixer)

    def showsComments(self, comments):
        label = LabelDriver.findSingle(self, QLabel,
                                       withBuddy(named(AlbumPage.COMMENTS_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = TextEditDriver.findSingle(self, QTextEdit, named(AlbumPage.COMMENTS_FIELD_NAME))
        edit.hasPlainText(comments)

    def addComments(self, *comments):
        edit = TextEditDriver.findSingle(self, QTextEdit, named(AlbumPage.COMMENTS_FIELD_NAME))
        for comment in comments:
            edit.addLine(comment)
        edit.clearFocus()

    def showsPrimaryStyle(self, style):
        label = LabelDriver.findSingle(self, QLabel,
                                       withBuddy(named(AlbumPage.PRIMARY_STYLE_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit, named(AlbumPage.PRIMARY_STYLE_FIELD_NAME))
        edit.isDisabled()
        edit.hasText(style)

    def showsMediaType(self, type_):
        label = LabelDriver.findSingle(self, QLabel,
                                       withBuddy(named(AlbumPage.MEDIA_TYPE_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit, named(AlbumPage.MEDIA_TYPE_FIELD_NAME))
        edit.isDisabled()
        edit.hasText(type_)

    def showsReleaseType(self, type_):
        label = LabelDriver.findSingle(self, QLabel,
                                       withBuddy(named(AlbumPage.RELEASE_TYPE_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit, named(AlbumPage.RELEASE_TYPE_FIELD_NAME))
        edit.isDisabled()
        edit.hasText(type_)