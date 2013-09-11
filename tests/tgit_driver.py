# -*- coding: utf-8 -*-

from PyQt4.Qt import QPushButton, QLabel, QFileDialog

import tgit.ui.main_window as main

from prober import EventProcessingProber
from matchers import named, showing_on_screen
from widgets import main_window
from widgets import (MainWindowDriver, PushButtonDriver, LabelDriver, FileDialogDriver)
from robot import Robot


class TGiTDriver(MainWindowDriver):
    def __init__(self, timeout_in_ms):
        super(TGiTDriver, self).__init__(
            main_window(named(main.MAIN_WINDOW_NAME), showing_on_screen()),
            EventProcessingProber(timeout_in_ms=timeout_in_ms))
        self._robot = Robot()

    def add_file(self, filename):
        self._open_file_dialog()
        self._enter_filename(filename)
        self._accept_file()

    def _open_file_dialog(self):
        add_file_button = PushButtonDriver.find(self, QPushButton,
                                                named(main.ADD_FILE_BUTTON_NAME))
        self._robot.perform(add_file_button.click())

    def _enter_filename(self, filename):
        self._robot.perform(self._file_dialog().enter_manually(filename))

    def _accept_file(self):
        self._robot.perform(self._file_dialog().accept())

    def shows_album_metadata(self, album_title):
        label = LabelDriver.find(self, QLabel, named(main.ALBUM_TITLE_INPUT_NAME))
        label.has_text(album_title)

    def _file_dialog(self):
        return FileDialogDriver.find(self, QFileDialog)

