# -*- coding: utf-8 -*-
import os

from PyQt5.QtWidgets import QFileDialog

from cute.matchers import named, disabled
from cute.widgets import window
from test.drivers.file_dialog_driver import FileDialogDriver


def save_as_dialog(parent):
    return SaveAsDialogDriver(window(QFileDialog, named("save_as_dialog")), parent.prober, parent.gesture_performer)


class SaveAsDialogDriver(FileDialogDriver):
    def save_as(self, filename):
        self.navigate_to_dir(os.path.dirname(filename))
        self.enter_manually(os.path.basename(filename))
        self.has_accept_button_text("&Save")
        self.accept()

    def rejects_selection_of(self, path):
        self.navigate_to_dir(os.path.dirname(path))
        self.select_file(os.path.basename(path))
        self.has_accept_button(disabled())
        self.reject()
