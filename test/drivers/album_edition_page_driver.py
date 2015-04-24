# -*- coding: utf-8 -*-

from cute.matchers import named, with_buddy, with_pixmap_height, with_pixmap_width
from test.drivers import BaseDriver
from test.drivers.picture_selection_dialog_driver import pictureSelectionDialog
from tgit.ui.album_edition_page import AlbumEditionPage


def album_edition_page(parent):
    return AlbumEditionPageDriver.find_single(parent, AlbumEditionPage, named('album-edition-page'))


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
        label.has_pixmap(with_pixmap_height(height))
        label.has_pixmap(with_pixmap_width(width))

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
        self.label(with_buddy(named('release-name'))).is_showing_on_screen()
        self.lineEdit(named('release-name')).has_text(name)

    def changeReleaseName(self, name):
        self.lineEdit(named('release-name')).change_text(name)

    def shows_compilation(self, value):
        self.label(with_buddy(named('compilation'))).is_showing_on_screen()
        compilation_checkbox = self.checkbox(named('compilation'))
        compilation_checkbox.is_checked(value)

    def toggle_compilation(self):
        compilation_checkbox = self.checkbox(named('compilation'))
        compilation_checkbox.click()

    def shows_lead_performer(self, name, disabled=False):
        label = self.label(with_buddy(named('lead-performer')))
        label.is_showing_on_screen()
        edit = self.lineEdit(named('lead-performer'))
        edit.has_text(name)
        edit.is_disabled(disabled)

    def showsISNI(self, name, disabled=False):
        label = self.label(with_buddy(named('isni')))
        label.is_showing_on_screen()
        label.is_disabled(disabled)
        edit = self.lineEdit(named('isni'))
        edit.has_text(name)
        edit.is_disabled(disabled)

    def enablesISNILookup(self, enabled=True):
        button = self.button(named('lookup-isni'))
        button.is_enabled(enabled)

    def enablesISNIAssign(self, enabled=True):
        button = self.button(named('assign-isni'))
        button.is_enabled(enabled)

    def changeLeadPerformer(self, name):
        self.lineEdit(named('lead-performer')).change_text(name)

    def showsGuestPerformers(self, names):
        self.label(with_buddy(named('guest-performers'))).is_showing_on_screen()
        self.lineEdit(named('guest-performers')).has_text(names)

    def changeGuestPerformers(self, names):
        self.lineEdit(named('guest-performers')).change_text(names)

    def showsLabelName(self, name):
        self.label(with_buddy(named('label-name'))).is_showing_on_screen()
        self.lineEdit(named('label-name')).has_text(name)

    def changeLabelName(self, name):
        self.lineEdit(named('label-name')).change_text(name)

    def showsArea(self, area):
        self.label(with_buddy(named('area'))).is_showing_on_screen()
        edit = self.lineEdit(named('area'))
        edit.is_disabled()
        edit.has_text(area)

    def showsCatalogNumber(self, number):
        self.label(with_buddy(named('catalog-number'))).is_showing_on_screen()
        self.lineEdit(named('catalog-number')).has_text(number)

    def changeCatalogNumber(self, number):
        self.lineEdit(named('catalog-number')).change_text(number)

    def showsUpc(self, code):
        self.label(with_buddy(named('upc'))).is_showing_on_screen()
        self.lineEdit(named('upc')).has_text(code)

    def changeUpc(self, code):
        self.lineEdit(named('upc')).change_text(code)

    def shows_recording_time(self, time):
        self.label(with_buddy(named('recording-time'))).is_showing_on_screen()
        self.lineEdit(named('recording-time')).has_text(time)

    def change_recording_time(self, time):
        self.lineEdit(named('recording-time')).change_text(time)

    def showsReleaseTime(self, time):
        self.label(with_buddy(named('release-time'))).is_showing_on_screen()
        self.lineEdit(named('release-time')).has_text(time)

    def changeReleaseTime(self, time):
        self.lineEdit(named('release-time')).change_text(time)

    def showsDigitalReleaseTime(self, time):
        self.label(with_buddy(named('digital-release-time'))).is_showing_on_screen()
        edit = self.lineEdit(named('digital-release-time'))
        edit.is_disabled()
        edit.has_text(time)

    def showsOriginalReleaseTime(self, time):
        self.label(with_buddy(named('original-release-time'))).is_showing_on_screen()
        self.lineEdit(named('original-release-time')).has_text(time)

    def changeOriginalReleaseTime(self, time):
        self.label(named('original-release-time')).change_text(time)

    def showsRecordingStudios(self, studios):
        self.label(with_buddy(named('recording-studios'))).is_showing_on_screen()
        self.lineEdit(named('recording-studios')).has_text(studios)

    def changeRecordingStudios(self, studios):
        self.lineEdit(named('recording-studios')).change_text(studios)

    def showsProducer(self, producer):
        self.label(with_buddy(named('producer'))).is_showing_on_screen()
        self.lineEdit(named('producer')).has_text(producer)

    def changeProducer(self, producer):
        self.lineEdit(named('producer')).change_text(producer)

    def showsMixer(self, mixer):
        self.label(with_buddy(named('mixer'))).is_showing_on_screen()
        self.lineEdit(named('mixer')).has_text(mixer)

    def changeMixer(self, mixer):
        self.lineEdit(named('mixer')).change_text(mixer)

    def showsComments(self, comments):
        self.label(with_buddy(named('comments'))).is_showing_on_screen()
        self.textEdit(named('comments')).has_plain_text(comments)

    def addComments(self, *comments):
        edit = self.textEdit(named('comments'))
        for comment in comments:
            edit.add_line(comment)
        edit.clear_focus()

    def shows_primary_style(self, style):
        self.label(with_buddy(named('primary-style'))).is_showing_on_screen()
        self.combobox(named('primary-style')).has_current_text(style)

    def changePrimaryStyle(self, style):
        self.combobox(named('primary-style')).change_text(style)

    def select_primary_style(self, style):
        self.combobox(named('primary-style')).select_option(style)

    def showsMediaType(self, type_):
        self.label(with_buddy(named('media-type'))).is_showing_on_screen()
        edit = self.lineEdit(named('media-type'))
        edit.is_disabled()
        edit.has_text(type_)

    def showsReleaseType(self, type_):
        self.label(with_buddy(named('release-type'))).is_showing_on_screen()
        edit = self.lineEdit(named('release-type'))
        edit.is_disabled()
        edit.has_text(type_)
