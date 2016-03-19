# -*- coding: utf-8 -*-
import os

from PyQt5.QtWidgets import QFileDialog

from cute.matchers import disabled
from cute.widgets import QFileDialogDriver, window


def file_selection_dialog(parent):
    return FileDialogDriver(window(QFileDialog), parent.prober, parent.gesture_performer)


class FileDialogDriver(QFileDialogDriver):
    def select(self, filename):
        self.is_active()
        self.view_as_list()
        self.navigate_to_dir(os.path.dirname(filename))
        self.select_file(os.path.basename(filename))
        self.accept()

    def rejects_selection_of(self, filename):
        self.is_active()
        self.navigate_to_dir(os.path.dirname(filename))
        self.select_file(os.path.basename(filename))
        self.has_accept_button(disabled())
        self.reject()
