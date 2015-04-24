# -*- coding: utf-8 -*-
import os

from PyQt5.QtWidgets import QFileDialog
from hamcrest import contains_string

from cute.matchers import named, disabled, showing_on_screen
from cute.widgets import FileDialogDriver, window


def track_selection_dialog(parent):
    return TrackSelectionDialogDriver(
        window(QFileDialog, named('track-selection-dialog'), showing_on_screen()), parent.prober,
        parent.gesture_performer)


class TrackSelectionDialogDriver(FileDialogDriver):
    def select_tracks_in_folder(self, folder):
        self.view_as_list()
        self.show_hidden_files()
        self.navigate_to_dir(folder)
        self.accept()

    def enter_track(self, filename):
        self.show_hidden_files()
        self.enter_manually(filename)
        self.accept()

    def select_tracks(self, *files, of_type='mp3'):
        if not files:
            return
        self.view_as_list()
        self.select_files_of_type(contains_string('*.{}'.format(of_type)))
        self.show_hidden_files()
        folder = os.path.dirname(files[0])
        self.navigate_to_dir(folder)
        self.select_files(*[os.path.basename(f) for f in files])
        self.accept()

    def rejects_selection_of(self, path):
        self.show_hidden_files()
        self.navigate_to_dir(os.path.dirname(path))
        self.select_file(os.path.basename(path))
        self.accept_button_is(disabled())
        self.reject()