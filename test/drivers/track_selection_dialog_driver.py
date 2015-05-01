# -*- coding: utf-8 -*-
import os

from PyQt5.QtWidgets import QFileDialog, QComboBox
from hamcrest import contains_string, contains

from cute.matchers import named, disabled, showing_on_screen
from cute.widgets import FileDialogDriver, window, ComboBoxDriver


def track_selection_dialog(parent):
    return TrackSelectionDialogDriver(
        window(QFileDialog, named("track-selection-dialog")), parent.prober, parent.gesture_performer)


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

    def select_tracks(self, *files):
        if not files:
            self.reject()

        self.view_as_list()
        self.show_hidden_files()
        self.navigate_to_dir(os.path.dirname(files[0]))
        self.select_files(*[os.path.basename(f) for f in files])
        self.accept()

    def rejects_selection_of(self, path):
        self.show_hidden_files()
        self.navigate_to_dir(os.path.dirname(path))
        self.select_file(os.path.basename(path))
        self.accept_button_is(disabled())
        self.reject()

    def shows_only_files(self, of_type):
        self.has_file_type_options(contains_string("*.{0}".format(of_type)))
        self.has_selected_file_type(contains_string("*.{0}".format(of_type)))
