# -*- coding: utf-8 -*-
from cute import gestures
from cute.widgets import WidgetDriver
from .album_screen_driver import album_screen
from .reference_track_selection_dialog_driver import reference_track_selection_dialog
from .load_album_dialog_driver import load_album_dialog
from .isni_lookup_dialog_driver import isni_lookup_dialog
from .message_box_driver import message_box
from .settings_dialog_driver import settings_dialog
from .menu_bar_driver import menu_bar
from .new_album_screen_driver import new_album_page
from .welcome_screen_driver import welcome_page


class MainWindowDriver(WidgetDriver):
    def __init__(self, selector, prober, gesture_performer):
        super().__init__(selector, prober, gesture_performer)

    def import_album(self, of_type, name, track_path, album_path):
        welcome_page(self).new_album(of_type)
        new_album_page(self).import_album(name, album_path, track_path)
        album_screen(self).is_showing_on_screen()

    def create_album(self, of_type, name, directory):
        welcome_page(self).new_album(of_type)
        new_album_page(self).create_empty_album(name, directory)
        album_screen(self).is_showing_on_screen()

    def add_tracks_in_folder(self):
        menu_bar(self).add_folder()

    def add_tracks_to_album(self, *paths, from_menu=False):
        if from_menu:
            menu_bar(self).add_files()
        else:
            album_screen(self).add_tracks_to_album(*paths)

    def move_track(self, title, to):
        album_screen(self).move_track(title, to)

    def remove_track(self, title):
        album_screen(self).remove_track(title)

    # todo have a quick navigation button
    def next(self):
        album_screen(self).nextPage()

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

    def tag_album(self):
        album_screen(self).tag()

    def change_settings(self, **settings):
        menu_bar(self).settings()
        settings_dialog(self).changeSettings(settings)
        message_box(self).ok()

    def has_settings(self, **settings):
        dialog = menu_bar(self).settings()
        try:
            dialog.showsSettings(settings)
        finally:
            dialog.close()

    def assign_isni_to_lead_performer(self):
        album_screen(self).assign_isni_to_lead_performer()

    def shows_assignation_failed(self):
        message_box(self).is_showing_on_screen()
        try:
            message_box(self).shows_message("Could not assign an ISNI")
            message_box(self).shows_details("invalid code creationRole eee")
        finally:
            message_box(self).ok()

    def find_isni_of_lead_performer(self):
        album_screen(self).lookup_isni_of_lead_performer()
        isni_lookup_dialog(self).select_first_identity()
        isni_lookup_dialog(self).accept()

    def shows_confirmation_message(self):
        try:
            message_box(self).is_showing_on_screen()
        finally:
            message_box(self).yes()

    def shows_welcome_screen(self):
        welcome_page(self).is_showing_on_screen()

    def has_disabled_album_actions(self):
        menu_bar(self).has_disabled_album_actions()

    def close_album(self, using_shortcut=False):
        if using_shortcut:
            self.click()
            self.perform(gestures.close())
        else:
            menu_bar(self).close_album()

    def export(self):
        menu_bar(self).export()

    def settings(self):
        menu_bar(self).settings()

    def load_album(self, filename):
        welcome_page(self).load()
        load_album_dialog(self).load(filename)
        album_screen(self).is_showing_on_screen()

    def save(self, using_shortcut=False):
        if using_shortcut:
            self.click()
            self.perform(gestures.save())
        else:
            menu_bar(self).save()
