# -*- coding: utf-8 -*-

from PyQt4.Qt import QPushButton

import tgit.ui.main_window as main

from events import MainEventLoop
from probing import EventProcessingProber
from matchers import named, showing_on_screen
from widgets import main_window, MainWindowDriver, PushButtonDriver
from robot import Robot


class TGiTDriver(MainWindowDriver):
    def __init__(self, timeout_in_ms):
        prober = EventProcessingProber(timeout_in_ms=timeout_in_ms)
        super(TGiTDriver, self).__init__(
            main_window(named(main.MAIN_WINDOW_NAME), showing_on_screen()),
            prober)
        self._robot = Robot()
        MainEventLoop.process_pending_events()

    def display_message(self):
        self._robot.perform(self._button(main.SURPRISE_BUTTON_NAME).press())
        # until we probe for a response, we need to wait for message to be printed to console
        MainEventLoop.process_events_for(50)

    def _button(self, button_name):
        return PushButtonDriver.find(self, QPushButton, named(button_name))
