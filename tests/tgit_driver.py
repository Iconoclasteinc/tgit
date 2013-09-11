# -*- coding: utf-8 -*-

import os
from PyQt4.Qt import QPushButton, QLineEdit, QFileDialog, QLabel

import tgit.ui.main_window as main

from prober import EventProcessingProber
from matchers import named, showing_on_screen
from widgets import main_window
from widgets import (MainWindowDriver, PushButtonDriver, LineEditDriver, LabelDriver,
                     FileDialogDriver)
from robot import Robot


class TGiTDriver(MainWindowDriver):
    def __init__(self, timeout_in_ms):
        super(TGiTDriver, self).__init__(
            main_window(named(main.MAIN_WINDOW_NAME), showing_on_screen()),
            EventProcessingProber(timeout_in_ms=timeout_in_ms))
        self._robot = Robot()

    def add_file(self, path):
        self._open_file_dialog()
        self._select_file(path)
        self._accept_file()

    def shows_album_metadata(self, album_title, bitrate):
        album_title_input = LineEditDriver.find(self, QLineEdit, named(main.ALBUM_TITLE_INPUT_NAME))
        album_title_input.has_text(album_title)
        bitrate_label = LabelDriver.find(self, QLabel, named(main.TRACK_BITRATE_TEXT_NAME))
        bitrate_label.has_text(bitrate)

    def _open_file_dialog(self):
        add_file_button = PushButtonDriver.find(self, QPushButton,
                                                named(main.ADD_FILE_BUTTON_NAME))
        self._robot.perform(add_file_button.click())

    def _select_file(self, path):
        dialog = FileDialogDriver.find(self, QFileDialog)
        self._robot.perform(dialog.navigate_to_dir(os.path.dirname(path)))
        self._robot.perform(dialog.select_file(os.path.basename(path)))

    def _accept_file(self):
        dialog = FileDialogDriver.find(self, QFileDialog)
        self._robot.perform(dialog.accept())
