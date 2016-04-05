# -*- coding: utf-8 -*-
import os

from PyQt5.QtWidgets import QFileDialog
from hamcrest import contains_string

from cute.matchers import named, disabled
from cute.widgets import window
from .file_dialog_driver import FileDialogDriver


def reference_track_selection_dialog(parent):
    return ReferenceTrackSelectionDialogDriver(
        window(QFileDialog, named("import_album_from_track_dialog")), parent.prober, parent.gesture_performer)


class ReferenceTrackSelectionDialogDriver(FileDialogDriver):
    def select_track(self, path, of_type="mp3"):
        self.filter_files_of_type(contains_string("*.{0}".format(of_type)))
        self.navigate_to_dir(os.path.dirname(path))
        self.select_file(os.path.basename(path))
        self.accept()

    def rejects_selection_of(self, path):
        self.navigate_to_dir(os.path.dirname(path))
        self.select_file(os.path.basename(path))
        self.has_accept_button(disabled())
        self.reject()
