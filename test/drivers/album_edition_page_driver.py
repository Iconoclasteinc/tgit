# -*- coding: utf-8 -*-

from PyQt4.QtGui import QWidget

from test.cute.matchers import named, withBuddy, withPixmapHeight, withPixmapWidth
from test.drivers.__base import BaseDriver
from test.drivers.picture_selection_dialog_driver import pictureSelectionDialog
from tgit.ui.album_edition_page import AlbumEditionPage


def albumEditionPage(parent):
    return AlbumEditionPageDriver.findSingle(parent, QWidget, named('album-edition-page'))


class AlbumEditionPageDriver(BaseDriver):
    def showsMetadata(self, **meta):
        for tag, value in meta.iteritems():
            if tag == 'releaseName':
                self.showsReleaseName(value)
            elif tag == 'leadPerformer':
                self.showsLeadPerformer(value)
            elif tag == 'guestPerformers':
                self.showsGuestPerformers(value)
            elif tag == 'labelName':
                self.showsLabelName(value)
            elif tag == 'catalogNumber':
                self.showsCatalogNumber(value)
            elif tag == 'upc':
                self.showsUpc(value)
            elif tag == 'recordingTime':
                self.showsRecordingTime(value)
            elif tag == 'releaseTime':
                self.showsReleaseTime(value)
            elif tag == 'originalReleaseTime':
                self.showsOriginalReleaseTime(value)
            elif tag == 'recordingStudios':
                self.showsRecordingStudios(value)
            elif tag == 'producer':
                self.showsProducer(value)
            elif tag == 'mixer':
                self.showsMixer(value)
            else:
                raise AssertionError("Don't know how to verify '%s'" % tag)

    def changeMetadata(self, **meta):
        for tag, value in meta.iteritems():
            if tag == 'frontCover':
                self.selectPicture(value)
            elif tag == 'releaseName':
                self.changeReleaseName(value)
            elif tag == 'leadPerformer':
                self.changeLeadPerformer(value)
            elif tag == 'guestPerformers':
                self.changeGuestPerformers(value)
            elif tag == 'labelName':
                self.changeLabelName(value)
            elif tag == 'catalogNumber':
                self.changeCatalogNumber(value)
            elif tag == 'upc':
                self.changeUpc(value)
            elif tag == 'recordingTime':
                self.changeRecordingTime(value)
            elif tag == 'releaseTime':
                self.changeReleaseTime(value)
            elif tag == 'originalReleaseTime':
                self.changeOriginalReleaseTime(value)
            elif tag == 'recordingStudios':
                self.changeRecordingStudios(value)
            elif tag == 'producer':
                self.changeProducer(value)
            elif tag == 'mixer':
                self.changeMixer(value)
            else:
                raise AssertionError("Don't know how to edit '%s'" % tag)

    def displaysPictureWithSize(self, width, height):
        label = self.label(named('front-cover'))
        label.isShowingOnScreen()
        label.hasPixmap(withPixmapHeight(height))
        label.hasPixmap(withPixmapWidth(width))

    def showsPicture(self):
        self.displaysPictureWithSize(*AlbumEditionPage.FRONT_COVER_SIZE)

    def showsPicturePlaceholder(self):
        self.displaysPictureWithSize(0, 0)

    def selectPicture(self, filename):
        self.addPicture()
        pictureSelectionDialog(self).selectPicture(filename)
        self.showsPicture()

    def addPicture(self):
        self.button(named('select-picture')).click()

    def removePicture(self):
        self.button(named('remove-picture')).click()

    def lookupISNI(self):
        self.button(named('lookup-isni')).click()

    def clearISNI(self):
        self.button(named('clear-isni')).click()

    def showsReleaseName(self, name):
        self.label(withBuddy(named('release-name'))).isShowingOnScreen()
        self.lineEdit(named('release-name')).hasText(name)

    def changeReleaseName(self, name):
        self.lineEdit(named('release-name')).changeText(name)

    def showsCompilation(self, flag):
        self.label(withBuddy(named('compilation'))).isShowingOnScreen()
        self.checkbox(named('compilation')).isChecked(flag)

    def toggleCompilation(self):
        self.checkbox(named('compilation')).click()

    def showsLeadPerformer(self, name, disabled=False):
        label = self.label(withBuddy(named('lead-performer')))
        label.isShowingOnScreen()
        edit = self.lineEdit(named('lead-performer'))
        edit.hasText(name)
        edit.isDisabled(disabled)

    def showsISNI(self, name, disabled=False):
        label = self.label(withBuddy(named('isni')))
        label.isShowingOnScreen()
        label.isDisabled(disabled)
        edit = self.lineEdit(named('isni'))
        edit.hasText(name)
        edit.isDisabled(disabled)

    def enablesISNILookup(self, enabled=True):
        button = self.button(named('lookup-isni'))
        button.isEnabled(enabled)

    def changeLeadPerformer(self, name):
        self.lineEdit(named('lead-performer')).changeText(name)

    def showsGuestPerformers(self, names):
        self.label(withBuddy(named('guest-performers'))).isShowingOnScreen()
        self.lineEdit(named('guest-performers')).hasText(names)

    def changeGuestPerformers(self, names):
        self.lineEdit(named('guest-performers')).changeText(names)

    def showsLabelName(self, name):
        self.label(withBuddy(named('label-name'))).isShowingOnScreen()
        self.lineEdit(named('label-name')).hasText(name)

    def changeLabelName(self, name):
        self.lineEdit(named('label-name')).changeText(name)

    def showsArea(self, area):
        self.label(withBuddy(named('area'))).isShowingOnScreen()
        edit = self.lineEdit(named('area'))
        edit.isDisabled()
        edit.hasText(area)

    def showsCatalogNumber(self, number):
        self.label(withBuddy(named('catalog-number'))).isShowingOnScreen()
        self.lineEdit(named('catalog-number')).hasText(number)

    def changeCatalogNumber(self, number):
        self.lineEdit(named('catalog-number')).changeText(number)

    def showsUpc(self, code):
        self.label(withBuddy(named('upc'))).isShowingOnScreen()
        self.lineEdit(named('upc')).hasText(code)

    def changeUpc(self, code):
        self.lineEdit(named('upc')).changeText(code)

    def showsRecordingTime(self, time):
        self.label(withBuddy(named('recording-time'))).isShowingOnScreen()
        self.lineEdit(named('recording-time')).hasText(time)

    def changeRecordingTime(self, time):
        self.lineEdit(named('recording-time')).changeText(time)

    def showsReleaseTime(self, time):
        self.label(withBuddy(named('release-time'))).isShowingOnScreen()
        self.lineEdit(named('release-time')).hasText(time)

    def changeReleaseTime(self, time):
        self.lineEdit(named('release-time')).changeText(time)

    def showsDigitalReleaseTime(self, time):
        self.label(withBuddy(named('digital-release-time'))).isShowingOnScreen()
        edit = self.lineEdit(named('digital-release-time'))
        edit.isDisabled()
        edit.hasText(time)

    def showsOriginalReleaseTime(self, time):
        self.label(withBuddy(named('original-release-time'))).isShowingOnScreen()
        self.lineEdit(named('original-release-time')).hasText(time)

    def changeOriginalReleaseTime(self, time):
        self.label(named('original-release-time')).changeText(time)

    def showsRecordingStudios(self, studios):
        self.label(withBuddy(named('recording-studios'))).isShowingOnScreen()
        self.lineEdit(named('recording-studios')).hasText(studios)

    def changeRecordingStudios(self, studios):
        self.lineEdit(named('recording-studios')).changeText(studios)

    def showsProducer(self, producer):
        self.label(withBuddy(named('producer'))).isShowingOnScreen()
        self.lineEdit(named('producer')).hasText(producer)

    def changeProducer(self, producer):
        self.lineEdit(named('producer')).changeText(producer)

    def showsMixer(self, mixer):
        self.label(withBuddy(named('mixer'))).isShowingOnScreen()
        self.lineEdit(named('mixer')).hasText(mixer)

    def changeMixer(self, mixer):
        self.lineEdit(named('mixer')).changeText(mixer)

    def showsComments(self, comments):
        self.label(withBuddy(named('comments'))).isShowingOnScreen()
        self.textEdit(named('comments')).hasPlainText(comments)

    def addComments(self, *comments):
        edit = self.textEdit(named('comments'))
        for comment in comments:
            edit.addLine(comment)
        edit.clearFocus()

    def showsPrimaryStyle(self, style):
        self.label(withBuddy(named('primary-style'))).isShowingOnScreen()
        self.combobox(named('primary-style')).hasCurrentText(style)

    def changePrimaryStyle(self, style):
        self.combobox(named('primary-style')).changeText(style)

    def selectPrimaryStyle(self, style):
        self.combobox(named('primary-style')).selectOption(style)

    def showsMediaType(self, type_):
        self.label(withBuddy(named('media-type'))).isShowingOnScreen()
        edit = self.lineEdit(named('media-type'))
        edit.isDisabled()
        edit.hasText(type_)

    def showsReleaseType(self, type_):
        self.label(withBuddy(named('release-type'))).isShowingOnScreen()
        edit = self.lineEdit(named('release-type'))
        edit.isDisabled()
        edit.hasText(type_)