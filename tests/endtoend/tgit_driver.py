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

    def add_file(self, path):
        self._open_add_file_dialog()
        self._select_file(path)
        self._accept_file()

    def shows_metadata(self, tags):
        self._front_cover_text_info_field().has_text(tags['front_cover_embedded_text'])
        self._release_name_input_field().has_text(tags['release_name'])
        self._lead_performer_input_field().has_text(tags['lead_performer'])
        self._track_title_input_field().has_text(tags['track_title'])
        self._version_info_input_field().has_text(tags['version_info'])
        self._bitrate_info_field().has_text(tags['bitrate'])
        self._track_duration_info_field().has_text(tags['duration'])

    def _open_add_file_dialog(self):
        add_file_button = AbstractButtonDriver.find(self, QPushButton,
                                                    named(main.ADD_FILE_BUTTON_NAME))
        add_file_button.click()

    def _select_file(self, path):
        dialog = FileDialogDriver.find(self, QFileDialog)
        dialog.show_hidden_files()
        dialog.navigate_to_dir(os.path.dirname(path))
        dialog.select_file(os.path.basename(path))

    def _accept_file(self):
        dialog = FileDialogDriver.find(self, QFileDialog)
        dialog.accept()

    def edit_metadata(self, tags):
        self._front_cover_picture_file_input_field().replace_all_text(
            tags['front_cover_picture'])
        self._release_name_input_field().replace_all_text(tags['release_name'])
        self._lead_performer_input_field().replace_all_text(tags['lead_performer'])
        self._track_title_input_field().replace_all_text(tags['track_title'])
        self._version_info_input_field().replace_all_text(tags['version_info'])

    def save_audio_file(self):
        save_button = AbstractButtonDriver.find(self, QPushButton, named(main.SAVE_BUTTON_NAME))
        save_button.click()

    def _front_cover_picture_file_input_field(self):
        return LineEditDriver.find(self, QLineEdit,
                                   named(main.FRONT_COVER_PICTURE_FILE_INPUT_NAME))

    def _front_cover_text_info_field(self):
        return LabelDriver.find(self, QLabel, named(main.FRONT_COVER_EMBEDDED_TEXT_INFO_NAME))

    def _release_name_input_field(self):
        return LineEditDriver.find(self, QLineEdit, named(main.RELEASE_NAME_INPUT_NAME))

    def _lead_performer_input_field(self):
        return LineEditDriver.find(self, QLineEdit, named(main.LEAD_PERFORMER_INPUT_NAME))

    def _track_title_input_field(self):
        return LineEditDriver.find(self, QLineEdit, named(main.TRACK_TITLE_INPUT_NAME))

    def _version_info_input_field(self):
        return LineEditDriver.find(self, QLineEdit, named(main.VERSION_INFO_INPUT_NAME))

    def _bitrate_info_field(self):
        return LabelDriver.find(self, QLabel, named(main.BITRATE_INFO_NAME))

    def _track_duration_info_field(self):
        return LabelDriver.find(self, QLabel, named(main.DURATION_INFO_NAME))
