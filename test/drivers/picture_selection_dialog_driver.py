# -*- coding: utf-8 -*-

import os

from PyQt5.QtWidgets import QFileDialog

from cute.matchers import named, disabled
from cute.widgets import FileDialogDriver, window


def picture_selection_dialog(parent):
    return PictureSelectionDialogDriver(
        window(QFileDialog, named('picture-selection-dialog')), parent.prober, parent.gesture_performer)


class PictureSelectionDialogDriver(FileDialogDriver):
    def select_picture(self, filename):
        self.view_as_list()
        self.navigate_to_dir(os.path.dirname(filename))
        self.select_file(os.path.basename(filename))
        self.accept()

    def rejects_selection_of(self, filename):
        self.navigate_to_dir(os.path.dirname(filename))
        self.select_file(os.path.basename(filename))
        self.accept_button_is(disabled())
        self.reject()