# -*- coding: utf-8 -*-

from cute.matchers import named, with_buddy, with_pixmap_height, with_pixmap_width
from tgit.ui.album_edition_page import AlbumEditionPage
from ._screen_driver import ScreenDriver
from .picture_selection_dialog_driver import picture_selection_dialog


def album_edition_page(parent):
    return AlbumEditionPageDriver.find_single(parent, AlbumEditionPage, named("album_edition_page"))


def no_album_edition_page(parent):
    return AlbumEditionPageDriver.find_none(parent, AlbumEditionPage, named("album_edition_page"))


class AlbumEditionPageDriver(ScreenDriver):
    def shows_metadata(self, **meta):
        for tag, value in meta.items():
            if tag == "release_name":
                self.shows_release_name(value)
            elif tag == "lead_performer":
                self.shows_lead_performer(value)
            elif tag == "compilation":
                self.shows_compilation(value)
            elif tag == "guest_performers":
                self.shows_guest_performers(value)
            elif tag == "label_name":
                self.shows_label_name(value)
            elif tag == "catalog_number":
                self.shows_catalog_number(value)
            elif tag == "upc":
                self.shows_upc(value)
            elif tag == "recording_time":
                self.shows_recording_time(value)
            elif tag == "release_time":
                self.shows_release_time(value)
            elif tag == "original_release_time":
                self.shows_original_release_time(value)
            elif tag == "isni":
                self.shows_isni(value, disabled=True)
            else:
                raise AssertionError("Don't know how to verify '{0}'".format(tag))

    def change_metadata(self, **meta):
        for tag, value in meta.items():
            if tag == "front_cover":
                self.select_picture(value)
            elif tag == "release_name":
                self.change_release_name(value)
            elif tag == "toggle_compilation" and value:
                self.toggle_compilation()
            elif tag == "lead_performer":
                self.change_lead_performer(value)
            elif tag == "guestPerformers":
                self.change_guest_performers(value)
            elif tag == "label_name":
                self.change_label_name(value)
            elif tag == "catalog_number":
                self.change_catalog_number(value)
            elif tag == "upc":
                self.change_upc(value)
            elif tag == "recording_time":
                self.change_recording_time(value)
            elif tag == "releaseTime":
                self.change_release_time(value)
            elif tag == "original_release_time":
                self.change_original_release_time(value)
            else:
                raise AssertionError("Don't know how to edit '{0}'".format(tag))

    def _displays_picture_with_size(self, width, height):
        label = self.label(named("front_cover"))
        label.is_showing_on_screen()
        label.has_pixmap(with_pixmap_height(height))
        label.has_pixmap(with_pixmap_width(width))

    def shows_picture(self):
        self._displays_picture_with_size(*AlbumEditionPage.FRONT_COVER_SIZE)

    def shows_picture_placeholder(self):
        self._displays_picture_with_size(*AlbumEditionPage.FRONT_COVER_SIZE)

    def select_picture(self, filename):
        self.add_picture()
        picture_selection_dialog(self).select_picture(filename)
        self.shows_picture()

    def add_picture(self):
        self.button(named("select_picture_button")).click()

    def remove_picture(self):
        self.button(named("remove_picture_button")).click()

    def clear_isni(self):
        self.button(named("clear_isni_button")).click()

    def assign_isni_to_lead_performer(self):
        self.button(named("assign_isni_button")).manipulate("enable", lambda button: button.setEnabled(True))
        self.button(named("assign_isni_button")).click()

    def lookup_isni_of_lead_performer(self):
        self.button(named("lookup_isni_button")).click()

    def edit_performers(self):
        self.button(named("add_guest_performers_button")).click()

    def shows_release_name(self, name):
        self.label(with_buddy(named("release_name"))).is_showing_on_screen()
        self.lineEdit(named("release_name")).has_text(name)

    def change_release_name(self, name):
        self.lineEdit(named("release_name")).change_text(name)

    def shows_compilation(self, value):
        self.label(with_buddy(named("compilation"))).is_showing_on_screen()
        compilation_checkbox = self.checkbox(named("compilation"))
        compilation_checkbox.is_checked(value)

    def toggle_compilation(self):
        compilation_checkbox = self.checkbox(named("compilation"))
        compilation_checkbox.click()

    def shows_lead_performer(self, name, disabled=False):
        label = self.label(with_buddy(named("lead_performer")))
        label.is_showing_on_screen()
        edit = self.lineEdit(named("lead_performer"))
        edit.has_text(name)
        edit.is_disabled(disabled)

    def shows_lead_performer_region(self, name):
        self.label(with_buddy(named("_lead_performer_region"))).is_showing_on_screen()
        edit = self.combobox(named("_lead_performer_region"))
        edit.has_current_text(name)

    def shows_isni(self, name, disabled=False):
        label = self.label(with_buddy(named("isni")))
        label.is_showing_on_screen()
        label.is_disabled(disabled)
        edit = self.lineEdit(named("isni"))
        edit.has_text(name)
        edit.is_disabled(disabled)

    def enables_isni_lookup(self, enabled=True):
        button = self.button(named("lookup_isni_button"))
        button.is_enabled(enabled)

    def disables_isni_assign(self):
        button = self.button(named("assign_isni_button"))
        button.is_disabled(True)

    def enables_isni_assign(self):
        button = self.button(named("assign_isni_button"))
        button.is_enabled(True)

    def isni_lookup_has_tooltip(self, text):
        self.button(named("lookup_isni_button")).has_tooltip(text)

    def change_lead_performer(self, name):
        self.lineEdit(named("lead_performer")).change_text(name)

    def change_lead_performer_region(self, name):
        self.combobox(named("_lead_performer_region")).select_option(name)

    def shows_guest_performers(self, names):
        self.label(with_buddy(named("guest_performers"))).is_showing_on_screen()
        self.lineEdit(named("guest_performers")).has_text(names)

    def change_guest_performers(self, names):
        self.lineEdit(named("guest_performers")).change_text(names)

    def shows_label_name(self, name):
        self.label(with_buddy(named("label_name"))).is_showing_on_screen()
        self.lineEdit(named("label_name")).has_text(name)

    def change_label_name(self, name):
        self.lineEdit(named("label_name")).change_text(name)

    def shows_catalog_number(self, number):
        self.label(with_buddy(named("catalog_number"))).is_showing_on_screen()
        self.lineEdit(named("catalog_number")).has_text(number)

    def change_catalog_number(self, number):
        self.lineEdit(named("catalog_number")).change_text(number)

    def shows_upc(self, code):
        self.label(with_buddy(named("barcode"))).is_showing_on_screen()
        self.lineEdit(named("barcode")).has_text(code)

    def change_upc(self, code):
        self.lineEdit(named("barcode")).change_text(code)

    def shows_recording_time(self, time):
        self.label(with_buddy(named("recording_time"))).is_showing_on_screen()
        self.dateEdit(named("recording_time")).has_date(time)

    def change_recording_time(self, year, month, day):
        self.dateEdit(named("recording_time")).change_date(year, month, day)

    def shows_release_time(self, time):
        self.label(with_buddy(named("release_time"))).is_showing_on_screen()
        self.dateEdit(named("release_time")).has_date(time)

    def change_release_time(self, year, month, day):
        self.dateEdit(named("release_time")).change_date(year, month, day)

    def shows_digital_release_time(self, time):
        self.label(with_buddy(named("digital_release_time"))).is_showing_on_screen()
        edit = self.dateEdit(named("digital_release_time"))
        edit.is_disabled()
        edit.has_date(time)

    def shows_original_release_time(self, time):
        self.label(with_buddy(named("original_release_time"))).is_showing_on_screen()
        self.dateEdit(named("original_release_time")).has_date(time)

    def change_original_release_time(self, time):
        self.label(named("original_release_time")).change_date(time)

    def shows_comments(self, comments):
        self.label(with_buddy(named("comments"))).is_showing_on_screen()
        self.textEdit(named("comments")).has_plain_text(comments)

    def add_comments(self, *comments):
        edit = self.textEdit(named("comments"))
        for comment in comments:
            edit.add_line(comment)
        edit.clear_focus()

    def shows_media_type(self, type_):
        self.label(with_buddy(named("media_type"))).is_showing_on_screen()
        edit = self.lineEdit(named("media_type"))
        edit.is_disabled()
        edit.has_text(type_)

    def shows_release_type(self, type_):
        self.label(with_buddy(named("release_type"))).is_showing_on_screen()
        edit = self.lineEdit(named("release_type"))
        edit.is_disabled()
        edit.has_text(type_)
