# -*- coding: utf-8 -*-
from cute.matchers import named, with_buddy, with_pixmap_size
from tgit.ui.pages.project_edition_page import ProjectEditionPage
from ._screen_driver import ScreenDriver
from .file_dialog_driver import file_selection_dialog


def project_edition_page(parent):
    return ProjectEditionPageDriver.find_single(parent, ProjectEditionPage, named("project_edition_page"))


def no_project_edition_page(parent):
    return ProjectEditionPageDriver.find_none(parent, ProjectEditionPage, named("project_edition_page"))


class ProjectEditionPageDriver(ScreenDriver):
    def shows_metadata(self, **meta):
        for tag, value in meta.items():
            if tag == "release_name":
                self.shows_title(value)
            elif tag == "lead_performer":
                self.shows_main_artist(value)
            elif tag == "compilation":
                self.shows_compilation(value)
            elif tag == "label_name":
                self.shows_label_name(value)
            elif tag == "catalog_number":
                self.shows_catalog_number(value)
            elif tag == "upc":
                self.shows_upc(value)
            elif tag == "release_time":
                self.shows_release_time(value)
            elif tag == "isni":
                self.shows_main_artist_isni(value)
            else:
                raise AssertionError("Don't know how to verify '{0}'".format(tag))

    def change_metadata(self, **meta):
        for tag, value in meta.items():
            if tag == "front_cover":
                self.select_artwork(value)
            elif tag == "release_name":
                self.change_title(value)
            elif tag == "toggle_compilation" and value:
                self.toggle_compilation()
            elif tag == "lead_performer":
                self.change_main_artist(value)
            elif tag == "label_name":
                self.change_label_name(value)
            elif tag == "catalog_number":
                self.change_catalog_number(value)
            elif tag == "upc":
                self.change_upc(value)
            elif tag == "releaseTime":
                self.change_release_time(value)
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
        self._displays_picture_with_size(*ProjectEditionPage.FRONT_COVER_SIZE)

    def shows_picture_placeholder(self):
        self._displays_picture_with_size(*ProjectEditionPage.FRONT_COVER_SIZE)

    def select_artwork(self, filename):
        self.add_artwork()
        file_selection_dialog(self).select(filename)
        self.shows_picture()

    def add_artwork(self):
        self.tool_button(named("_select_artwork_button")).click()

    def remove_artwork(self):
        self.tool_button(named("_remove_artwork_button")).click()

    def lookup_isni_of_main_artist(self):
        self.tool_button(named("_main_artist_isni_actions_button")).click()

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

    def shows_main_artist_region(self, name, disabled=False):
        self.label(with_buddy(named("_main_artist_region"))).is_showing_on_screen()
        edit = self.combobox(named("_main_artist_region"))
        edit.has_current_text(name)
        edit.is_disabled(disabled)

    def shows_main_artist_isni(self, name, disabled=False):
        edit = self.lineEdit(named("_main_artist_isni"))
        edit.has_text(name)
        edit.is_disabled(disabled)
        self.label(named("_main_artist_isni_help")).is_disabled(disabled)

    def shows_main_artist_isni_lookup_button(self, disabled=False):
        self.tool_button(named("_main_artist_isni_actions_button")).is_disabled(disabled)

    def shows_main_artist_isni_assign_action(self, disabled=True):
        menu = self.tool_button(named("_main_artist_isni_actions_button")).open_menu()
        menu.menu_item(named("_main_artist_isni_assign_action")).is_disabled(disabled)

    def change_main_artist(self, name):
        self.lineEdit(named("_main_artist")).change_text(name)

    def change_main_artist_isni(self, isni):
        self.lineEdit(named("_main_artist_isni")).change_text(isni)

    def change_main_artist_region(self, name):
        self.combobox(named("_main_artist_region")).select_option(name)

    def shows_label_name(self, name):
        self._select_release_tab()
        self.label(with_buddy(named("_label_name"))).is_showing_on_screen()
        self.lineEdit(named("_label_name")).has_text(name)

    def _select_release_tab(self):
        self.tabs(named("_tabs")).select("2. Release")

    def change_label_name(self, name):
        self._select_release_tab()
        self.lineEdit(named("_label_name")).change_text(name)

    def shows_catalog_number(self, number):
        self._select_release_tab()
        self.label(with_buddy(named("_catalog_number"))).is_showing_on_screen()
        self.lineEdit(named("_catalog_number")).has_text(number)

    def change_catalog_number(self, number):
        self._select_release_tab()
        self.lineEdit(named("_catalog_number")).change_text(number)

    def shows_upc(self, code):
        self._select_release_tab()
        self.label(with_buddy(named("_barcode"))).is_showing_on_screen()
        self.lineEdit(named("_barcode")).has_text(code)

    def change_upc(self, code):
        self._select_release_tab()
        self.lineEdit(named("_barcode")).change_text(code)

    def shows_release_time(self, time):
        self._select_release_tab()
        self.label(with_buddy(named("_release_time"))).is_showing_on_screen()
        self.dateEdit(named("_release_time")).has_date(time)

    def change_release_time(self, year, month, day):
        self._select_release_tab()
        self.dateEdit(named("_release_time")).enter_date(year, month, day)

    def shows_media_type(self, type_):
        self._select_release_tab()
        self.label(with_buddy(named("_media_type"))).is_showing_on_screen()
        edit = self.lineEdit(named("_media_type"))
        edit.is_disabled()
        edit.has_text(type_)

    def shows_release_type(self, type_):
        self._select_release_tab()
        self.label(with_buddy(named("_release_type"))).is_showing_on_screen()
        edit = self.lineEdit(named("_release_type"))
        edit.is_disabled()
        edit.has_text(type_)
