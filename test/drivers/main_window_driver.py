# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog

from cute import gestures
from cute.widgets import WidgetDriver
from test.drivers.save_as_dialog_driver import save_as_dialog
from test.drivers.sign_in_dialog_driver import sign_in_dialog
from .isni_assignation_review_dialog_driver import isni_assignation_review_dialog
from .isni_lookup_dialog_driver import isni_lookup_dialog
from .load_album_dialog_driver import load_project_dialog
from .menu_bar_driver import menu_bar
from .message_box_driver import message_box
from .new_project_page_driver import new_project_page
from .project_screen_driver import project_screen
from .user_preferences_dialog_driver import user_preferences_dialog
from .welcome_page_driver import welcome_page


class MainWindowDriver(WidgetDriver):
    def __init__(self, selector, prober, gesture_performer):
        super().__init__(selector, prober, gesture_performer)

    def create_project(self, of_type, name, location, import_from=""):
        welcome_page(self).new_project(of_type)
        new_project_page(self).create_project(name, location, import_from=import_from)
        project_screen(self).is_showing_on_screen()

    def add_tracks_in_folder(self):
        menu_bar(self).file.add_folder()

    def add_tracks_to_project(self, from_menu=False):
        if from_menu:
            menu_bar(self).file.add_files()
        else:
            project_screen(self).add_tracks_to_project()

    def move_track(self, title, to):
        project_screen(self).move_track(title, to)

    def remove_track(self, title):
        project_screen(self).remove_track(title)

    # todo have a quick navigation button
    def next(self):
        project_screen(self).to_next_page()

    def navigate_to_project_page(self):
        menu_bar(self).navigate.to_project_page()

    def navigate_to_track_page(self, title, track_number):
        menu_bar(self).navigate.to_track_page(title, track_number)

    def shows_project_contains(self, *tracks):
        project_screen(self).shows_project_contains(*tracks)

    def shows_project_metadata(self, **tags):
        project_screen(self).shows_project_metadata(**tags)

    def edit_project_metadata(self, **tags):
        project_screen(self).edit_project_metadata(**tags)

    def shows_track_metadata(self, **tags):
        project_screen(self).shows_track_metadata(**tags)

    def edit_track_metadata(self, **tags):
        project_screen(self).edit_track_metadata(**tags)

    def change_settings(self, **settings):
        menu_bar(self).file.settings()
        user_preferences_dialog(self).change_preferences(settings)
        message_box(self).click_ok()

    def has_settings(self, **settings):
        dialog = menu_bar(self).file.settings()
        try:
            dialog.shows_preferences(settings)
        finally:
            dialog.close()

    def assign_isni_to_main_artist(self):
        project_screen(self).lookup_isni_of_main_artist()
        isni_lookup_dialog(self).assign()
        isni_assignation_review_dialog(self).select_individual()
        isni_assignation_review_dialog(self).click_ok()

    def shows_assignation_failed(self):
        message_box(self).is_active()
        message_box(self).click_ok()

    def find_isni_of_main_artist(self, name):
        project_screen(self).lookup_isni_of_main_artist()
        isni_lookup_dialog(self).select_identity(name)
        isni_lookup_dialog(self).accept()

    def shows_welcome_screen(self):
        welcome_page(self).is_showing_on_screen()

    def shows_track_menu_item(self, title, track_number):
        menu_bar(self).navigate.shows_track_action(title, track_number)

    def does_not_show_menu_item(self, title, track_number):
        menu_bar(self).navigate.does_not_show_action(title, track_number)

    def has_disabled_project_actions(self):
        menu_bar(self).file.has_disabled_project_actions()
        menu_bar(self).navigate.is_disabled()
        menu_bar(self).transmit.is_disabled()

    def close_project(self, using_shortcut=False):
        if using_shortcut:
            self.click()
            self.perform(gestures.close())
        else:
            menu_bar(self).file.close_project()

    def export(self):
        menu_bar(self).file.export()

    def settings(self):
        menu_bar(self).file.settings()

    def load_project(self, filename):
        welcome_page(self).load()
        load_project_dialog(self).load(filename)
        project_screen(self).is_showing_on_screen()

    def shows_recent_projects(self, *entries):
        welcome_page(self).shows_recent_projects(*entries)

    def open_recent_project(self, name):
        welcome_page(self).open_recent_project(name)
        project_screen(self).is_showing_on_screen()

    def save(self, using_shortcut=False):
        if using_shortcut:
            self.click()
            self.perform(gestures.save())
        else:
            menu_bar(self).file.save()

    def about_qt(self):
        menu_bar(self).help.about_qt()

    def about(self):
        menu_bar(self).help.about()

    def help(self):
        menu_bar(self).help.online_help()

    def request_feature(self):
        menu_bar(self).help.request_feature()

    def register(self):
        menu_bar(self).account.register()

    def sign_in(self):
        menu_bar(self).account.sign_in()

    def sign_in_as(self, username, password):
        self.sign_in()
        sign_in_dialog(self).sign_in_with(username, password)
        WidgetDriver.find_none(self, QDialog).exists()

    def is_signed_in_as(self, email):
        menu_bar(self).account.shows_signed_in_user(email)

    def sign_out(self):
        menu_bar(self).account.sign_out()

    def is_signed_out(self):
        menu_bar(self).account.shows_sign_in_menu()

    def declare_project_to_soproq(self, filename):
        self.transmit_to_soproq()
        save_as_dialog(self).save_as(filename)
        message_box(self).click_ok()

    def transmit_to_soproq(self):
        menu_bar(self).transmit.soproq()
