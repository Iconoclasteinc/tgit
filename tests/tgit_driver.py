# -*- coding: utf-8 -*-

import tgit.ui.main as main

from probing import EventProcessingProber
from matchers import named, showing_on_screen
from widgets import main_window, MainWindowDriver

class TGiTDriver(MainWindowDriver):
    def __init__(self, timeout):
        super(TGiTDriver, self).__init__(
            main_window(named(main.MAIN_WINDOW_NAME), showing_on_screen()),
            EventProcessingProber(timeout=timeout))