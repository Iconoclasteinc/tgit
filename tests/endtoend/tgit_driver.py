# -*- coding: utf-8 -*-

import os
from PyQt4.Qt import QPushButton, QLineEdit, QFileDialog, QLabel

from tests.cute.prober import EventProcessingProber
from tests.cute.matchers import named, showing_on_screen
from tests.cute.widgets import main_window
from tests.cute.widgets import (MainWindowDriver, AbstractButtonDriver, LineEditDriver, LabelDriver,
                                FileDialogDriver)
from tests.cute.robot import Robot

import tgit.ui.main_window as main


class TGiTDriver(MainWindowDriver):
    def __init__(self, timeout_in_ms):
        super(TGiTDriver, self).__init__(
            main_window(named(main.MAIN_WINDOW_NAME), showing_on_screen()),
            EventProcessingProber(timeout_in_ms=timeout_in_ms),
            Robot())

    def import_track(self, path):
        self._open_import_track_dialog()
        self._select_track(path)

    def shows_metadata(self, tags):
        self._front_cover_embedded_text().has_text(tags['front_cover_embedded_text'])
        self._release_name().has_text(tags['release_name'])
        self._lead_performer().has_text(tags['lead_performer'])
        self._original_release_date().has_text(tags['original_release_date'])
        self._upc().has_text(tags['upc'])
        self._track_title().has_text(tags['track_title'])
        self._featured_guest().has_text(tags['featured_guest'])
        self._version_info().has_text(tags['version_info'])
        self._isrc().has_text(tags['isrc'])
        self._bitrate().has_text(tags['bitrate'])
        self._track_duration().has_text(tags['duration'])

    def _open_import_track_dialog(self):
        add_file_button = AbstractButtonDriver.find(self, QPushButton,
                                                    named(main.ADD_FILE_BUTTON_NAME))
        add_file_button.click()

    def _select_track(self, track_file):
        dialog = self._add_file_dialog()
        dialog.show_hidden_files()
        dialog.navigate_to_dir(os.path.dirname(track_file))
        dialog.select_file(os.path.basename(track_file))
        dialog.accept()

    def _add_file_dialog(self):
        return FileDialogDriver.find(self, QFileDialog, named(main.IMPORT_TRACK_DIALOG_NAME))

    def edit_metadata(self, tags):
        self._load_picture(tags['front_cover_picture'])
        self._release_name().replace_all_text(tags['release_name'])
        self._lead_performer().replace_all_text(tags['lead_performer'])
        self._original_release_date().replace_all_text(tags['original_release_date'])
        self._upc().replace_all_text(tags['upc'])
        self._track_title().replace_all_text(tags['track_title'])
        self._version_info().replace_all_text(tags['version_info'])
        self._featured_guest().replace_all_text(tags['featured_guest'])
        self._isrc().replace_all_text(tags['isrc'])

    def _load_picture(self, picture_file):
        self._open_select_picture_dialog()
        self._select_picture(picture_file)

    def _open_select_picture_dialog(self):
        select_picture_button = AbstractButtonDriver.find(self, QPushButton,
                                                          named(main.SELECT_PICTURE_BUTTON_NAME))
        select_picture_button.click()

    def _select_picture(self, picture_file):
        select_picture_dialog = self._select_picture_dialog()
        select_picture_dialog.navigate_to_dir(os.path.dirname(picture_file))
        select_picture_dialog.select_file(os.path.basename(picture_file))
        select_picture_dialog.accept()

    def _select_picture_dialog(self):
        return FileDialogDriver.find(self, QFileDialog, named(main.SELECT_PICTURE_DIALOG_NAME))

    def save_audio_file(self):
        save_button = AbstractButtonDriver.find(self, QPushButton, named(main.SAVE_BUTTON_NAME))
        save_button.click()

    def _front_cover_picture(self):
        return LineEditDriver.find(self, QLineEdit, named(main.FRONT_COVER_PICTURE_FILE_NAME))

    def _front_cover_embedded_text(self):
        return LabelDriver.find(self, QLabel, named(main.FRONT_COVER_EMBEDDED_TEXT_NAME))

    def _release_name(self):
        return LineEditDriver.find(self, QLineEdit, named(main.RELEASE_NAME_NAME))

    def _lead_performer(self):
        return LineEditDriver.find(self, QLineEdit, named(main.LEAD_PERFORMER_NAME))

    def _original_release_date(self):
        return LineEditDriver.find(self, QLineEdit, named(main.ORIGINAL_RELEASE_DATE_NAME))

    def _upc(self):
        return LineEditDriver.find(self, QLineEdit, named(main.UPC_NAME))

    def _track_title(self):
        return LineEditDriver.find(self, QLineEdit, named(main.TRACK_TITLE_NAME))

    def _version_info(self):
        return LineEditDriver.find(self, QLineEdit, named(main.VERSION_INFO_NAME))

    def _featured_guest(self):
        return LineEditDriver.find(self, QLineEdit, named(main.FEATURED_GUEST_NAME))

    def _isrc(self):
        return LineEditDriver.find(self, QLineEdit, named(main.ISRC_NAME))

    def _bitrate(self):
        return LabelDriver.find(self, QLabel, named(main.BITRATE_NAME))

    def _track_duration(self):
        return LabelDriver.find(self, QLabel, named(main.DURATION_NAME))