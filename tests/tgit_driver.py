# -*- coding: utf-8 -*-

from PyQt4.Qt import QPushButton, QLabel

import tgit.ui.main_window as main

from events import MainEventLoop
from prober import EventProcessingProber
from matchers import named, showing_on_screen
from widgets import main_window, MainWindowDriver, PushButtonDriver, LabelDriver
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

    def display_message(self):
        self._robot.perform(self._button(main.OPEN_FILE_BUTTON_NAME).click())
        # until we probe for a response, we need to wait for message to be printed to console
        MainEventLoop.process_events_for(50)

    def _button(self, button_name):
        return PushButtonDriver.find(self, QPushButton, named(button_name))

    def open_file(self, filename):
        #dialog = QFileDialog(main)
        #dialog.setOption(QFileDialog.DontUseNativeDialog)
        #dialog.setModal(True)
        #dialog.show()
        self._robot.perform(self._button(main.OPEN_FILE_BUTTON_NAME).click())

    def shows_music_title(self, title):
        label = LabelDriver.find(self, QLabel, named(main.TITLE_LABEL_NAME))
        label.has_text('Ma préférence')

