# -*- coding: utf-8 -*-
import os

from PyQt5.QtWidgets import QFileDialog

from cute.matchers import named, disabled
from cute.widgets import window, QFileDialogDriver


def load_project_dialog(parent):
    return LoadProjectDialogDriver(window(QFileDialog, named("load_project_dialog")), parent.prober,
                                   parent.gesture_performer)


class LoadProjectDialogDriver(QFileDialogDriver):
    def load(self, filename):
        self.show_hidden_files()
        self.view_as_list()
        self.navigate_to_dir(os.path.dirname(filename))
        self.select_file(os.path.basename(filename))
        self.accept()

    def rejects_selection_of(self, filename):
        self.view_as_list()
        self.navigate_to_dir(os.path.dirname(filename))
        self.select_file(os.path.basename(filename))
        self.has_accept_button(disabled())
        self.reject()
