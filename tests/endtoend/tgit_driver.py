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
        self._album_title_input_field().has_text(tags['album'])
        self._album_artist_input_field().has_text(tags['artist'])
        self._track_title_input_field().has_text(tags['track'])
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
        self._album_title_input_field().replace_all_text(tags['album'])
        self._album_artist_input_field().replace_all_text(tags['artist'])
        self._track_title_input_field().replace_all_text(tags['track'])
        self._version_info_input_field().replace_all_text(tags['version_info'])

    def save_audio_file(self):
        save_button = AbstractButtonDriver.find(self, QPushButton, named(main.SAVE_BUTTON_NAME))
        save_button.click()

    def _album_title_input_field(self):
        return LineEditDriver.find(self, QLineEdit, named(main.ALBUM_TITLE_INPUT_NAME))

    def _album_artist_input_field(self):
        return LineEditDriver.find(self, QLineEdit, named(main.ALBUM_ARTIST_INPUT_NAME))

    def _track_title_input_field(self):
        return LineEditDriver.find(self, QLineEdit, named(main.TRACK_TITLE_INPUT_NAME))

    def _version_info_input_field(self):
        return LineEditDriver.find(self, QLineEdit, named(main.VERSION_INFO_INPUT_NAME))

    def _bitrate_info_field(self):
        return LabelDriver.find(self, QLabel, named(main.BITRATE_INFO_NAME))

    def _track_duration_info_field(self):
        return LabelDriver.find(self, QLabel, named(main.DURATION_INFO_NAME))
