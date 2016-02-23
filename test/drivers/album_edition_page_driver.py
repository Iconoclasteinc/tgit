# -*- coding: utf-8 -*-

from cute.matchers import named, with_buddy, with_pixmap_size
from test.drivers.artist_table_driver import musician_table_driver
from tgit.ui.pages.album_edition_page import AlbumEditionPage
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
                self.shows_title(value)
            elif tag == "lead_performer":
                self.shows_main_artist(value)
            elif tag == "compilation":
                self.shows_compilation(value)
            elif tag == "guest_performers":
                self.shows_artists(value)
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
                self.shows_main_artist_isni(value)
            else:
                raise AssertionError("Don't know how to verify '{0}'".format(tag))

    def change_metadata(self, **meta):
        for tag, value in meta.items():
            if tag == "front_cover":
                self.select_picture(value)
            elif tag == "release_name":
                self.change_title(value)
            elif tag == "toggle_compilation" and value:
                self.toggle_compilation()
            elif tag == "lead_performer":
                self.change_main_artist(value)
            elif tag == "guestPerformers":
                self.change_artists(value)
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
            elif tag == "isni":
                pass
            else:
                raise AssertionError("Don't know how to edit '{0}'".format(tag))

        if "isni" in meta:
            self.change_main_artist_isni(meta["isni"])

    def _displays_picture_with_size(self, width, height):
        label = self.label(named("_front_cover"))
        label.is_showing_on_screen()
        label.has_pixmap(with_pixmap_size(width, height))

    def shows_picture(self):
        self._displays_picture_with_size(*AlbumEditionPage.FRONT_COVER_SIZE)

    def shows_picture_placeholder(self):
        self._displays_picture_with_size(*AlbumEditionPage.FRONT_COVER_SIZE)

    def select_picture(self, filename):
        self.add_picture()
        picture_selection_dialog(self).select_picture(filename)
        self.shows_picture()

    def add_picture(self):
        self.button(named("_select_picture_button")).click()

    def remove_picture(self):
        self.button(named("_remove_picture_button")).click()

    def assign_isni_to_main_artist(self):
        menu = self.tool_button(named("_main_artist_isni_actions_button")).open_menu()
        menu.select_menu_item(named("_main_artist_isni_assign_action"))

    def confirm_isni(self):
        self.lineEdit(named("_main_artist_isni")).enter()

    def lookup_isni_of_main_artist(self):
        self.tool_button(named("_main_artist_isni_actions_button")).click()

    def edit_performers(self):
        self.tabs(named("_tabs")).select("Artists")
        self.button(named("_add_artist_button")).click()

    def shows_title(self, name):
        self.label(with_buddy(named("_title"))).is_showing_on_screen()
        self.lineEdit(named("_title")).has_text(name)

    def change_title(self, name):
        self.lineEdit(named("_title")).change_text(name)

    def shows_compilation(self, value):
        compilation_checkbox = self.checkbox(named("_compilation"))
        compilation_checkbox.is_checked(value)

    def toggle_compilation(self):
        compilation_checkbox = self.checkbox(named("_compilation"))
        compilation_checkbox.click()

    def shows_main_artist(self, name, disabled=False):
        label = self.label(with_buddy(named("_main_artist")))
        label.is_showing_on_screen()
        edit = self.lineEdit(named("_main_artist"))
        edit.has_text(name)
        edit.is_disabled(disabled)

    def shows_main_artist_region(self, name):
        self.label(with_buddy(named("_main_artist_region"))).is_showing_on_screen()
        edit = self.combobox(named("_main_artist_region"))
        edit.has_current_text(name)

    def shows_main_artist_isni(self, name):
        self.tool_button(named("_main_artist_isni_actions_button")).is_showing_on_screen()
        self.lineEdit(named("_main_artist_isni")).has_text(name)

    def enables_main_artist_isni_lookup(self, enabled=True):
        self.tool_button(named("_main_artist_isni_actions_button")).is_enabled(enabled)

    def disables_main_artist_isni_assign(self):
        menu = self.tool_button(named("_main_artist_isni_actions_button")).open_menu()
        menu.menu_item(named("_main_artist_isni_assign_action")).is_disabled(True)

    def main_artist_isni_lookup_has_tooltip(self, text):
        self.tool_button(named("_main_artist_isni_actions_button")).has_tooltip(text)

    def change_main_artist(self, name):
        self.lineEdit(named("_main_artist")).change_text(name)

    def change_main_artist_isni(self, isni):
        self.lineEdit(named("_main_artist_isni")).change_text(isni)

    def change_main_artist_region(self, name):
        self.combobox(named("_main_artist_region")).select_option(name)

    def shows_only_musicians_in_table(self, *musicians):
        self.tabs(named("_tabs")).select("2. Musicians")
        musician_table_driver(self).shows_only_musicians_in_table(*musicians)

    def remove_musician(self, row):
        self.tabs(named("_tabs")).select("2. Musicians")
        musician_table_driver(self).remove_musician(row)

    def add_musician(self, instrument, name, row):
        self.tabs(named("_tabs")).select("2. Musicians")
        self.button(named("_add_musician_button")).click()
        musician_table_driver(self).add_musician(instrument, name, row)

    def change_instrument_of_row(self, row, text):
        self.tabs(named("_tabs")).select("2. Musicians")
        musician_table_driver(self).change_instrument_of_row(row, text)

    def change_musician_of_row(self, row, text):
        self.tabs(named("_tabs")).select("2. Musicians")
        musician_table_driver(self).change_musician_of_row(row, text)

    def shows_label_name(self, name):
        self.tabs(named("_tabs")).select("1. Record")
        self.label(with_buddy(named("_label_name"))).is_showing_on_screen()
        self.lineEdit(named("_label_name")).has_text(name)

    def change_label_name(self, name):
        self.tabs(named("_tabs")).select("1. Record")
        self.lineEdit(named("_label_name")).change_text(name)

    def shows_catalog_number(self, number):
        self.tabs(named("_tabs")).select("1. Record")
        self.label(with_buddy(named("_catalog_number"))).is_showing_on_screen()
        self.lineEdit(named("_catalog_number")).has_text(number)

    def change_catalog_number(self, number):
        self.tabs(named("_tabs")).select("1. Record")
        self.lineEdit(named("_catalog_number")).change_text(number)

    def shows_upc(self, code):
        self.tabs(named("_tabs")).select("1. Record")
        self.label(with_buddy(named("_barcode"))).is_showing_on_screen()
        self.lineEdit(named("_barcode")).has_text(code)

    def change_upc(self, code):
        self.tabs(named("_tabs")).select("1. Record")
        self.lineEdit(named("_barcode")).change_text(code)

    def shows_recording_time(self, time):
        self.tabs(named("_tabs")).select("3. Dates")
        self.label(with_buddy(named("_recording_time"))).is_showing_on_screen()
        self.dateEdit(named("_recording_time")).has_date(time)

    def change_recording_time(self, year, month, day):
        self.tabs(named("_tabs")).select("3. Dates")
        self.dateEdit(named("_recording_time")).enter_date(year, month, day)

    def shows_release_time(self, time):
        self.tabs(named("_tabs")).select("3. Dates")
        self.label(with_buddy(named("_release_time"))).is_showing_on_screen()
        self.dateEdit(named("_release_time")).has_date(time)

    def change_release_time(self, year, month, day):
        self.tabs(named("_tabs")).select("3. Dates")
        self.dateEdit(named("_release_time")).enter_date(year, month, day)

    def shows_digital_release_time(self, time):
        self.tabs(named("_tabs")).select("3. Dates")
        self.label(with_buddy(named("_digital_release_time"))).is_showing_on_screen()
        edit = self.dateEdit(named("_digital_release_time"))
        edit.is_disabled()
        edit.has_date(time)

    def shows_original_release_time(self, time):
        self.tabs(named("_tabs")).select("3. Dates")
        self.label(with_buddy(named("_original_release_time"))).is_showing_on_screen()
        self.dateEdit(named("_original_release_time")).has_date(time)

    def change_original_release_time(self, time):
        self.tabs(named("_tabs")).select("3. Dates")
        self.label(named("_original_release_time")).enter_date(time)

    def shows_comments(self, comments):
        self.tabs(named("_tabs")).select("1. Record")
        self.label(with_buddy(named("_comments"))).is_showing_on_screen()
        self.textEdit(named("_comments")).has_plain_text(comments)

    def add_comments(self, *comments):
        self.tabs(named("_tabs")).select("1. Record")
        edit = self.textEdit(named("_comments"))
        for comment in comments:
            edit.add_line(comment)
        edit.clear_focus()

    def shows_media_type(self, type_):
        self.tabs(named("_tabs")).select("1. Record")
        self.label(with_buddy(named("_media_type"))).is_showing_on_screen()
        edit = self.lineEdit(named("_media_type"))
        edit.is_disabled()
        edit.has_text(type_)

    def shows_release_type(self, type_):
        self.tabs(named("_tabs")).select("1. Record")
        self.label(with_buddy(named("_release_type"))).is_showing_on_screen()
        edit = self.lineEdit(named("_release_type"))
        edit.is_disabled()
        edit.has_text(type_)
