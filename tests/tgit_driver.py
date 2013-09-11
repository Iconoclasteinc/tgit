# -*- coding: utf-8 -*-

from PyQt4.Qt import QPushButton, QLabel, QLineEdit, QFileDialog

import tgit.ui.main_window as main

from events import MainEventLoop
from prober import EventProcessingProber
from matchers import named, with_text, showing_on_screen
from widgets import main_window
from widgets import (MainWindowDriver, PushButtonDriver, LabelDriver, LineEditDriver,
                     WidgetDriver)
from robot import Robot


class TGiTDriver(MainWindowDriver):
    def __init__(self, timeout_in_ms):
        super(TGiTDriver, self).__init__(
            main_window(named(main.MAIN_WINDOW_NAME), showing_on_screen()),
            EventProcessingProber(timeout_in_ms=timeout_in_ms))
        self._robot = Robot()
        self._wait_for_window_shown()

    def _wait_for_window_shown(self):
        MainEventLoop.process_pending_events()

    def open_file(self, filename):
        self.open_file_dialog()
        self.enter_manually(filename)
        self.accept()

    def open_file_dialog(self):
        open_file_button = PushButtonDriver.find(self, QPushButton,
                                                 named(main.OPEN_FILE_BUTTON_NAME))
        self._robot.perform(open_file_button.click())

    def enter_manually(self, filename):
        dialog = WidgetDriver.find(self, QFileDialog)
        filename_input = LineEditDriver.find(dialog, QLineEdit, named("fileNameEdit"))
        self._robot.perform(filename_input.replace_text(filename))

    def accept(self):
        dialog = WidgetDriver.find(self, QFileDialog)
        accept_button = PushButtonDriver.find(dialog, QPushButton, with_text("&Open"))
        self._robot.perform(accept_button.click())

    def shows_music_title(self, title):
        label = LabelDriver.find(self, QLabel, named(main.TITLE_LABEL_NAME))
        label.has_text('Ma préférence')

