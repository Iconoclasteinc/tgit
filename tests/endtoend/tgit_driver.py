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

    def shows_album_metadata(self, album_title, bitrate, duration):
        album_title_input = LineEditDriver.find(self, QLineEdit, named(main.ALBUM_TITLE_INPUT_NAME))
        album_title_input.has_text(album_title)
        bitrate_info = LabelDriver.find(self, QLabel, named(main.BITRATE_INFO_NAME))
        bitrate_info.has_text(bitrate)
        duration_info = LabelDriver.find(self, QLabel, named(main.DURATION_INFO_NAME))
        duration_info.has_text(duration)

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

    def edit_metadata(self, album):
        album_title_input = LineEditDriver.find(self, QLineEdit, named(main.ALBUM_TITLE_INPUT_NAME))
        album_title_input.focus_with_mouse()
        album_title_input.replace_all_text(album)

    def save_audio_file(self):
        save_button = AbstractButtonDriver.find(self, QPushButton, named(main.SAVE_BUTTON_NAME))
        save_button.click()
