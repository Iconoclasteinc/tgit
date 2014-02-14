# -*- coding: utf-8 -*-

from PyQt4.QtGui import QLabel, QLineEdit, QPushButton, QPlainTextEdit, QWidget, QCheckBox

from test.cute.matchers import named, withBuddy, withPixmapHeight, withPixmapWidth
from test.cute.widgets import (WidgetDriver, LabelDriver, LineEditDriver,
                               ButtonDriver, TextEditDriver)
from test.drivers.picture_selection_dialog_driver import pictureSelectionDialog

import tgit.tags as tags
from tgit.ui.views.album_edition_page import AlbumEditionPage


def albumEditionPage(parent):
    return AlbumEditionPageDriver.findSingle(parent, QWidget, named(AlbumEditionPage.NAME))


class AlbumEditionPageDriver(WidgetDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(AlbumEditionPageDriver, self).__init__(selector, prober, gesturePerformer)

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
                self.selectPicture(value)
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

    def _displaysPictureWithSize(self, width, height):
        label = self._label(named(AlbumEditionPage.FRONT_COVER_FIELD_NAME))
        label.isShowingOnScreen()
        label.hasPixmap(withPixmapHeight(height))
        label.hasPixmap(withPixmapWidth(width))

    def showsPicture(self):
        self._displaysPictureWithSize(*AlbumEditionPage.FRONT_COVER_SIZE)

    def showsPicturePlaceholder(self):
        self._displaysPictureWithSize(0, 0)

    def selectPicture(self, filename):
        self.addPicture()
        pictureSelectionDialog(self).selectPicture(filename)
        self.showsPicture()

    def _button(self, matching):
        return ButtonDriver.findSingle(self, QPushButton, matching)

    def addPicture(self):
        button = self._button(named(AlbumEditionPage.SELECT_PICTURE_BUTTON_NAME))
        button.click()

    def removePicture(self):
        button = self._button(named(AlbumEditionPage.REMOVE_PICTURE_BUTTON_NAME))
        button.click()

    def showsReleaseName(self, name):
        label = self._label(withBuddy(named(AlbumEditionPage.RELEASE_NAME_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(AlbumEditionPage.RELEASE_NAME_FIELD_NAME))
        edit.hasText(name)

    def changeReleaseName(self, name):
        edit = self._lineEdit(named(AlbumEditionPage.RELEASE_NAME_FIELD_NAME))
        edit.changeText(name)

    def showsCompilation(self, flag):
        label = self._label(withBuddy(named(AlbumEditionPage.COMPILATION_FIELD_NAME)))
        label.isShowingOnScreen()
        checkbox = self._checkbox(named(AlbumEditionPage.COMPILATION_FIELD_NAME))
        checkbox.isChecked(flag)

    def toggleCompilation(self):
        checkbox = self._checkbox(named(AlbumEditionPage.COMPILATION_FIELD_NAME))
        checkbox.click()

    def showsLeadPerformer(self, name):
        label = self._label(withBuddy(named(AlbumEditionPage.LEAD_PERFORMER_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(AlbumEditionPage.LEAD_PERFORMER_FIELD_NAME))
        edit.hasText(name)

    def changeLeadPerformer(self, name):
        edit = self._lineEdit(named(AlbumEditionPage.LEAD_PERFORMER_FIELD_NAME))
        edit.changeText(name)

    def showsGuestPerformers(self, names):
        label = self._label(withBuddy(named(AlbumEditionPage.GUEST_PERFORMERS_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(AlbumEditionPage.GUEST_PERFORMERS_FIELD_NAME))
        edit.hasText(names)

    def changeGuestPerformers(self, names):
        edit = self._lineEdit(named(AlbumEditionPage.GUEST_PERFORMERS_FIELD_NAME))
        edit.changeText(names)

    def showsLabelName(self, name):
        label = self._label(withBuddy(named(AlbumEditionPage.LABEL_NAME_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(AlbumEditionPage.LABEL_NAME_FIELD_NAME))
        edit.hasText(name)

    def changeLabelName(self, name):
        edit = self._lineEdit(named(AlbumEditionPage.LABEL_NAME_FIELD_NAME))
        edit.changeText(name)

    def showsLabelTerritory(self, town):
        label = self._label(withBuddy(named(AlbumEditionPage.LABEL_TERRITORY_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(AlbumEditionPage.LABEL_TERRITORY_FIELD_NAME))
        edit.isDisabled()
        edit.hasText(town)

    def showsArea(self, area):
        label = self._label(withBuddy(named(AlbumEditionPage.AREA_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(AlbumEditionPage.AREA_FIELD_NAME))
        edit.isDisabled()
        edit.hasText(area)

    def showsCatalogNumber(self, number):
        label = self._label(withBuddy(named(AlbumEditionPage.CATALOG_NUMBER_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(AlbumEditionPage.CATALOG_NUMBER_FIELD_NAME))
        edit.hasText(number)

    def changeCatalogNumber(self, number):
        edit = self._lineEdit(named(AlbumEditionPage.CATALOG_NUMBER_FIELD_NAME))
        edit.changeText(number)

    def showsUpc(self, code):
        label = self._label(withBuddy(named(AlbumEditionPage.UPC_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(AlbumEditionPage.UPC_FIELD_NAME))
        edit.hasText(code)

    def changeUpc(self, code):
        edit = self._lineEdit(named(AlbumEditionPage.UPC_FIELD_NAME))
        edit.changeText(code)

    def showsRecordingTime(self, time):
        label = self._label(withBuddy(named(AlbumEditionPage.RECORDING_TIME_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(AlbumEditionPage.RECORDING_TIME_FIELD_NAME))
        edit.hasText(time)

    def changeRecordingTime(self, time):
        edit = self._lineEdit(named(AlbumEditionPage.RECORDING_TIME_FIELD_NAME))
        edit.changeText(time)

    def showsReleaseTime(self, time):
        label = self._label(withBuddy(named(AlbumEditionPage.RELEASE_TIME_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(AlbumEditionPage.RELEASE_TIME_FIELD_NAME))
        edit.hasText(time)

    def changeReleaseTime(self, time):
        edit = self._lineEdit(named(AlbumEditionPage.RELEASE_TIME_FIELD_NAME))
        edit.changeText(time)

    def showsDigitalReleaseTime(self, time):
        label = self._label(withBuddy(named(AlbumEditionPage.DIGITAL_RELEASE_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(AlbumEditionPage.DIGITAL_RELEASE_FIELD_NAME))
        edit.isDisabled()
        edit.hasText(time)

    def showsOriginalReleaseTime(self, time):
        label = self._label(withBuddy(named(AlbumEditionPage.ORIGINAL_RELEASE_TIME_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(AlbumEditionPage.ORIGINAL_RELEASE_TIME_FIELD_NAME))
        edit.hasText(time)

    def changeOriginalReleaseTime(self, time):
        edit = self._label(named(AlbumEditionPage.ORIGINAL_RELEASE_TIME_FIELD_NAME))
        edit.changeText(time)

    def showsRecordingStudios(self, studios):
        label = self._label(withBuddy(named(AlbumEditionPage.RECORDING_STUDIOS_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(AlbumEditionPage.RECORDING_STUDIOS_FIELD_NAME))
        edit.hasText(studios)

    def changeRecordingStudios(self, studios):
        edit = self._lineEdit(named(AlbumEditionPage.RECORDING_STUDIOS_FIELD_NAME))
        edit.changeText(studios)

    def showsProducer(self, producer):
        label = self._label(withBuddy(named(AlbumEditionPage.PRODUCER_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(AlbumEditionPage.PRODUCER_FIELD_NAME))
        edit.hasText(producer)

    def changeProducer(self, producer):
        edit = LineEditDriver.findSingle(self, QLineEdit, named(AlbumEditionPage.PRODUCER_FIELD_NAME))
        edit.changeText(producer)

    def showsMixer(self, mixer):
        label = self._label(withBuddy(named(AlbumEditionPage.MIXER_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(AlbumEditionPage.MIXER_FIELD_NAME))
        edit.hasText(mixer)

    def changeMixer(self, mixer):
        edit = self._lineEdit(named(AlbumEditionPage.MIXER_FIELD_NAME))
        edit.changeText(mixer)

    def showsComments(self, comments):
        label = self._label(withBuddy(named(AlbumEditionPage.COMMENTS_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._textEdit(named(AlbumEditionPage.COMMENTS_FIELD_NAME))
        edit.hasPlainText(comments)

    def addComments(self, *comments):
        edit = self._textEdit(named(AlbumEditionPage.COMMENTS_FIELD_NAME))
        for comment in comments:
            edit.addLine(comment)
        edit.clearFocus()

    def showsPrimaryStyle(self, style):
        label = self._label(withBuddy(named(AlbumEditionPage.PRIMARY_STYLE_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(AlbumEditionPage.PRIMARY_STYLE_FIELD_NAME))
        edit.hasText(style)

    def changePrimaryStyle(self, style):
        edit = self._lineEdit(named(AlbumEditionPage.PRIMARY_STYLE_FIELD_NAME))
        edit.changeText(style)

    def showsMediaType(self, type_):
        label = self._label(withBuddy(named(AlbumEditionPage.MEDIA_TYPE_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(AlbumEditionPage.MEDIA_TYPE_FIELD_NAME))
        edit.isDisabled()
        edit.hasText(type_)

    def showsReleaseType(self, type_):
        label = self._label(withBuddy(named(AlbumEditionPage.RELEASE_TYPE_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(AlbumEditionPage.RELEASE_TYPE_FIELD_NAME))
        edit.isDisabled()
        edit.hasText(type_)

    def _label(self, matching):
        return LabelDriver.findSingle(self, QLabel, matching)

    def _lineEdit(self, matching):
        return LineEditDriver.findSingle(self, QLineEdit, matching)

    def _textEdit(self, matching):
        return TextEditDriver.findSingle(self, QPlainTextEdit, matching)

    def _checkbox(self, matching):
        return ButtonDriver.findSingle(self, QCheckBox, matching)