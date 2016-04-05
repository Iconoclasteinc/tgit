# -*- coding: utf-8 -*-
import os

from PyQt5.QtWidgets import QFileDialog

from cute.matchers import named, disabled
from cute.widgets import window
from .file_dialog_driver import FileDialogDriver


def load_project_dialog(parent):
    return LoadProjectDialogDriver(window(QFileDialog, named("load_project_dialog")), parent.prober,
                                   parent.gesture_performer)


class LoadProjectDialogDriver(FileDialogDriver):
    def load(self, filename):
        self.navigate_to_dir(os.path.dirname(filename))
        self.select_file(os.path.basename(filename))
        self.accept()

    def rejects_selection_of(self, filename):
        self.navigate_to_dir(os.path.dirname(filename))
        self.select_file(os.path.basename(filename))
        self.has_accept_button(disabled())
        self.reject()
