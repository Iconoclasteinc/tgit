# -*- coding: utf-8 -*-
from cute import gestures
from cute.widgets import WidgetDriver
from .album_screen_driver import album_screen
from .load_album_dialog_driver import load_album_dialog
from .isni_lookup_dialog_driver import isni_lookup_dialog
from .message_box_driver import message_box
from .settings_dialog_driver import settings_dialog
from .menu_bar_driver import menu_bar
from .new_album_page_driver import new_album_page
from test.drivers import export_as_dialog, track_selection_dialog
from .welcome_screen_driver import welcome_page


class MainWindowDriver(WidgetDriver):
    def __init__(self, selector, prober, gesture_performer):
        super().__init__(selector, prober, gesture_performer)

    def create_album(self, of_type, name, location, import_from=""):
        welcome_page(self).new_album()
        new_album_page(self).create_album(of_type, name, location, import_from=import_from)
        album_screen(self).is_showing_on_screen()

    def add_tracks_in_folder(self):
        menu_bar(self).file.add_folder()

    def add_tracks_to_album(self, *paths, from_menu=False):
        if from_menu:
            menu_bar(self).file.add_files()
            track_selection_dialog(self).select_tracks(*paths)
        else:
            album_screen(self).add_tracks_to_album(*paths)

    def move_track(self, title, to):
        album_screen(self).move_track(title, to)

    def remove_track(self, title):
        album_screen(self).remove_track(title)

    # todo have a quick navigation button
    def next(self):
        album_screen(self).nextPage()

    def navigate_to_composition_page(self):
        menu_bar(self).navigate.to_composition_page()

    def navigate_to_album_page(self):
        menu_bar(self).navigate.to_album_page()

    def navigate_to_track_page(self, title, track_number):
        menu_bar(self).navigate.to_track_page(title, track_number)

    def shows_album_contains(self, *tracks):
        album_screen(self).shows_album_contains(*tracks)

    def shows_album_metadata(self, **tags):
        album_screen(self).shows_album_metadata(**tags)

    def edit_album_metadata(self, **tags):
        album_screen(self).edit_album_metadata(**tags)

    def shows_track_metadata(self, **tags):
        album_screen(self).shows_track_metadata(**tags)

    def editTrackMetadata(self, **tags):
        album_screen(self).edit_track_metadata(**tags)

    def change_settings(self, **settings):
        menu_bar(self).file.settings()
        settings_dialog(self).changeSettings(settings)
        message_box(self).ok()

    def has_settings(self, **settings):
        dialog = menu_bar(self).file.settings()
        try:
            dialog.showsSettings(settings)
        finally:
            dialog.close()

    def assign_isni_to_lead_performer(self):
        album_screen(self).assign_isni_to_lead_performer()

    def shows_assignation_failed(self):
        message_box(self).is_active()
        try:
            message_box(self).shows_message("Could not assign an ISNI")
            message_box(self).shows_details("invalid code creationRole eee")
        finally:
            message_box(self).ok()

    def find_isni_of_lead_performer(self):
        album_screen(self).lookup_isni_of_lead_performer()
        isni_lookup_dialog(self).select_first_identity()
        isni_lookup_dialog(self).accept()

    def shows_welcome_screen(self):
        welcome_page(self).is_showing_on_screen()

    def shows_track_menu_item(self, title, track_number):
        menu_bar(self).navigate.shows_track_action(title, track_number)

    def does_not_show_menu_item(self, title, track_number):
        menu_bar(self).navigate.does_not_show_action(title, track_number)

    def has_disabled_album_actions(self):
        menu_bar(self).file.has_disabled_album_actions()
        menu_bar(self).navigate.is_disabled()

    def close_album(self, using_shortcut=False):
        if using_shortcut:
            self.click()
            self.perform(gestures.close())
        else:
            menu_bar(self).file.close_album()
        message_box(self).is_showing_on_screen()
        message_box(self).yes()

    def export(self, filename):
        menu_bar(self).file.export()
        export_as_dialog(self). export_as(filename)

    def settings(self):
        menu_bar(self).file.settings()

    def load_album(self, filename):
        welcome_page(self).load()
        load_album_dialog(self).load(filename)
        album_screen(self).is_showing_on_screen()

    def save(self, using_shortcut=False):
        if using_shortcut:
            self.click()
            self.perform(gestures.save())
        else:
            menu_bar(self).file.save()
