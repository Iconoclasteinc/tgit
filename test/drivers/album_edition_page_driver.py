# -*- coding: utf-8 -*-

from test.cute.matchers import named, withBuddy, withPixmapHeight, withPixmapWidth
from test.drivers import BaseDriver
from test.drivers.picture_selection_dialog_driver import pictureSelectionDialog
from tgit.ui.album_edition_page import AlbumEditionPage


def album_edition_page(parent):
    return AlbumEditionPageDriver.findSingle(parent, AlbumEditionPage, named('album-edition-page'))


class AlbumEditionPageDriver(BaseDriver):
    def shows_metadata(self, **meta):
        for tag, value in meta.items():
            if tag == 'release_name':
                self.showsReleaseName(value)
            elif tag == 'lead_performer':
                self.shows_lead_performer(value)
            elif tag == 'compilation':
                self.shows_compilation(value)
            elif tag == 'guestPerformers':
                self.showsGuestPerformers(value)
            elif tag == 'label_name':
                self.showsLabelName(value)
            elif tag == 'catalogNumber':
                self.showsCatalogNumber(value)
            elif tag == 'upc':
                self.showsUpc(value)
            elif tag == 'recording_time':
                self.shows_recording_time(value)
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
            elif tag == 'primary_style':
                self.shows_primary_style(value)
            else:
                raise AssertionError("Don't know how to verify '%s'" % tag)

    def change_metadata(self, **meta):
        for tag, value in meta.items():
            if tag == 'front_cover':
                self.select_picture(value)
            elif tag == 'release_name':
                self.changeReleaseName(value)
            elif tag == 'toggle_compilation' and value:
                self.toggle_compilation()
            elif tag == 'lead_performer':
                self.changeLeadPerformer(value)
            elif tag == 'guestPerformers':
                self.changeGuestPerformers(value)
            elif tag == 'label_name':
                self.changeLabelName(value)
            elif tag == 'catalogNumber':
                self.changeCatalogNumber(value)
            elif tag == 'upc':
                self.changeUpc(value)
            elif tag == 'recording_time':
                self.change_recording_time(value)
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
            elif tag == 'primary_style':
                self.select_primary_style(value)
            else:
                raise AssertionError("Don't know how to edit '%s'" % tag)

    def displaysPictureWithSize(self, width, height):
        label = self.label(named('front-cover'))
        label.is_showing_on_screen()
        label.hasPixmap(withPixmapHeight(height))
        label.hasPixmap(withPixmapWidth(width))

    def showsPicture(self):
        self.displaysPictureWithSize(*AlbumEditionPage.FRONT_COVER_SIZE)

    def showsPicturePlaceholder(self):
        self.displaysPictureWithSize(0, 0)

    def select_picture(self, filename):
        self.addPicture()
        pictureSelectionDialog(self).selectPicture(filename)
        self.showsPicture()

    def addPicture(self):
        self.button(named('select-picture')).click()

    def removePicture(self):
        self.button(named('remove-picture')).click()

    def clear_isni(self):
        self.button(named('clear-isni')).click()

    def assign_isni_to_lead_performer(self):
        self.button(named('assign-isni')).click()

    def lookup_isni_of_lead_performer(self):
        self.button(named('lookup-isni')).click()

    def addPerformer(self):
        self.button(named('add-performer')).click()

    def showsReleaseName(self, name):
        self.label(withBuddy(named('release-name'))).is_showing_on_screen()
        self.lineEdit(named('release-name')).hasText(name)

    def changeReleaseName(self, name):
        self.lineEdit(named('release-name')).changeText(name)

    def shows_compilation(self, value):
        self.label(withBuddy(named('compilation'))).is_showing_on_screen()
        compilation_checkbox = self.checkbox(named('compilation'))
        compilation_checkbox.is_checked(value)

    def toggle_compilation(self):
        compilation_checkbox = self.checkbox(named('compilation'))
        compilation_checkbox.click()

    def shows_lead_performer(self, name, disabled=False):
        label = self.label(withBuddy(named('lead-performer')))
        label.is_showing_on_screen()
        edit = self.lineEdit(named('lead-performer'))
        edit.hasText(name)
        edit.is_disabled(disabled)

    def showsISNI(self, name, disabled=False):
        label = self.label(withBuddy(named('isni')))
        label.is_showing_on_screen()
        label.is_disabled(disabled)
        edit = self.lineEdit(named('isni'))
        edit.hasText(name)
        edit.is_disabled(disabled)

    def enablesISNILookup(self, enabled=True):
        button = self.button(named('lookup-isni'))
        button.is_enabled(enabled)

    def enablesISNIAssign(self, enabled=True):
        button = self.button(named('assign-isni'))
        button.is_enabled(enabled)

    def changeLeadPerformer(self, name):
        self.lineEdit(named('lead-performer')).changeText(name)

    def showsGuestPerformers(self, names):
        self.label(withBuddy(named('guest-performers'))).is_showing_on_screen()
        self.lineEdit(named('guest-performers')).hasText(names)

    def changeGuestPerformers(self, names):
        self.lineEdit(named('guest-performers')).changeText(names)

    def showsLabelName(self, name):
        self.label(withBuddy(named('label-name'))).is_showing_on_screen()
        self.lineEdit(named('label-name')).hasText(name)

    def changeLabelName(self, name):
        self.lineEdit(named('label-name')).changeText(name)

    def showsArea(self, area):
        self.label(withBuddy(named('area'))).is_showing_on_screen()
        edit = self.lineEdit(named('area'))
        edit.is_disabled()
        edit.hasText(area)

    def showsCatalogNumber(self, number):
        self.label(withBuddy(named('catalog-number'))).is_showing_on_screen()
        self.lineEdit(named('catalog-number')).hasText(number)

    def changeCatalogNumber(self, number):
        self.lineEdit(named('catalog-number')).changeText(number)

    def showsUpc(self, code):
        self.label(withBuddy(named('upc'))).is_showing_on_screen()
        self.lineEdit(named('upc')).hasText(code)

    def changeUpc(self, code):
        self.lineEdit(named('upc')).changeText(code)

    def shows_recording_time(self, time):
        self.label(withBuddy(named('recording-time'))).is_showing_on_screen()
        self.lineEdit(named('recording-time')).hasText(time)

    def change_recording_time(self, time):
        self.lineEdit(named('recording-time')).changeText(time)

    def showsReleaseTime(self, time):
        self.label(withBuddy(named('release-time'))).is_showing_on_screen()
        self.lineEdit(named('release-time')).hasText(time)

    def changeReleaseTime(self, time):
        self.lineEdit(named('release-time')).changeText(time)

    def showsDigitalReleaseTime(self, time):
        self.label(withBuddy(named('digital-release-time'))).is_showing_on_screen()
        edit = self.lineEdit(named('digital-release-time'))
        edit.is_disabled()
        edit.hasText(time)

    def showsOriginalReleaseTime(self, time):
        self.label(withBuddy(named('original-release-time'))).is_showing_on_screen()
        self.lineEdit(named('original-release-time')).hasText(time)

    def changeOriginalReleaseTime(self, time):
        self.label(named('original-release-time')).changeText(time)

    def showsRecordingStudios(self, studios):
        self.label(withBuddy(named('recording-studios'))).is_showing_on_screen()
        self.lineEdit(named('recording-studios')).hasText(studios)

    def changeRecordingStudios(self, studios):
        self.lineEdit(named('recording-studios')).changeText(studios)

    def showsProducer(self, producer):
        self.label(withBuddy(named('producer'))).is_showing_on_screen()
        self.lineEdit(named('producer')).hasText(producer)

    def changeProducer(self, producer):
        self.lineEdit(named('producer')).changeText(producer)

    def showsMixer(self, mixer):
        self.label(withBuddy(named('mixer'))).is_showing_on_screen()
        self.lineEdit(named('mixer')).hasText(mixer)

    def changeMixer(self, mixer):
        self.lineEdit(named('mixer')).changeText(mixer)

    def showsComments(self, comments):
        self.label(withBuddy(named('comments'))).is_showing_on_screen()
        self.textEdit(named('comments')).hasPlainText(comments)

    def addComments(self, *comments):
        edit = self.textEdit(named('comments'))
        for comment in comments:
            edit.addLine(comment)
        edit.clearFocus()

    def shows_primary_style(self, style):
        self.label(withBuddy(named('primary-style'))).is_showing_on_screen()
        self.combobox(named('primary-style')).has_current_text(style)

    def changePrimaryStyle(self, style):
        self.combobox(named('primary-style')).changeText(style)

    def select_primary_style(self, style):
        self.combobox(named('primary-style')).select_option(style)

    def showsMediaType(self, type_):
        self.label(withBuddy(named('media-type'))).is_showing_on_screen()
        edit = self.lineEdit(named('media-type'))
        edit.is_disabled()
        edit.hasText(type_)

    def showsReleaseType(self, type_):
        self.label(withBuddy(named('release-type'))).is_showing_on_screen()
        edit = self.lineEdit(named('release-type'))
        edit.is_disabled()
        edit.hasText(type_)
