# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QAbstractButton

from cute import matchers as match
from cute.matchers import showing_on_screen, with_text
from cute.widgets import MainWindowDriver, WidgetDriver, ButtonDriver
from test.drivers.export_as_dialog_driver import export_as_dialog
from test.drivers.isni_error_message_box_driver import message_box
from test.drivers.isni_lookup_dialog_driver import isni_lookup_dialog
from test.drivers.menu_bar_driver import menu_bar
from test.drivers.album_screen_driver import album_screen
from test.drivers.settings_dialog_driver import settings_dialog
from test.drivers.track_selection_dialog_driver import track_selection_dialog
from test.drivers.welcome_screen_driver import welcome_screen


class TaggerDriver(MainWindowDriver):
    def __init__(self, selector, prober, gesture_performer):
        super(TaggerDriver, self).__init__(selector, prober, gesture_performer)

    def enterAudioFile(self, filename):
        track_selection_dialog(self).enter_track(filename)

    def select_audio_files(self, *paths, of_type):
        track_selection_dialog(self).select_tracks(*paths, of_type=of_type)

    def cancelSelection(self):
        track_selection_dialog(self).cancel()

    def create_album(self):
        welcome_screen(self).new_album()
        self.shows_album_screen()

    def showsWelcomeScreen(self):
        welcome_screen(self).is_showing_on_screen()

    def shows_album_screen(self):
        album_screen(self).is_showing_on_screen()

    def showsExportAsDialog(self):
        export_as_dialog(self).is_showing_on_screen()

    def removeTrack(self, title):
        album_screen(self).removeTrack(title)

    def moveTrack(self, title, to):
        album_screen(self).moveTrack(title, to)

    # todo have a quick navigation button
    def next(self):
        album_screen(self).nextPage()

    def showsAlbumContains(self, *tracks):
        album_screen(self).showsAlbumContains(*tracks)

    def shows_album_metadata(self, **tags):
        album_screen(self).shows_album_metadata(**tags)

    def edit_album_metadata(self, **tags):
        album_screen(self).edit_album_metadata(**tags)

    def shows_track_metadata(self, **tags):
        album_screen(self).shows_track_metadata(**tags)

    def editTrackMetadata(self, **tags):
        album_screen(self).edit_track_metadata(**tags)

    def save_album(self):
        album_screen(self).save()

    def change_settings(self, **settings):
        menu_bar(self).settings()
        settings_dialog(self).changeSettings(settings)
        self.acknowledge()

    def hasSettings(self, **settings):
        dialog = menu_bar(self).settings()
        try:
            dialog.showsSettings(settings)
        finally:
            dialog.close()

    def acknowledge(self):
        ok = ButtonDriver.find_single(self.restart_message(), QAbstractButton, with_text("OK"))
        ok.click()

    def assign_isni_to_lead_performer(self):
        album_screen(self).assign_isni_to_lead_performer()

    def tries_to_assign_isni_to_lead_performer_with_invalid_data(self):
        album_screen(self).assign_isni_to_lead_performer()
        message_box(self).is_showing_on_screen()

        try:
            message_box(self).is_showing_message("Could not assign an ISNI")
            message_box(self).is_showing_details("Invalid data: invalid code creationRole eee")
        finally:
            message_box(self).acknowledge()

    def finds_isni_of_lead_performer(self):
        album_screen(self).lookup_isni_of_lead_performer()
        isni_lookup_dialog(self).selects_first_identity()
        isni_lookup_dialog(self).confirm()

    def restart_message(self):
        return WidgetDriver.find_single(self, QDialog, match.named("restart-message"), showing_on_screen())
