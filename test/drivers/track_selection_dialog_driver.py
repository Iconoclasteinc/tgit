# -*- coding: utf-8 -*-
import os

from PyQt5.QtWidgets import QFileDialog
from hamcrest import starts_with, contains_string

from test.cute.matchers import named, disabled, showingOnScreen
from test.cute.widgets import FileDialogDriver, window


def track_selection_dialog(parent):
    return TrackSelectionDialogDriver(
        window(QFileDialog, named('track-selection-dialog'), showingOnScreen()), parent.prober, parent.gesturePerformer)


class TrackSelectionDialogDriver(FileDialogDriver):
    def select_tracks_in_folder(self, folder):
        self.view_as_list()
        self.showHiddenFiles()
        self.navigateToDir(folder)
        self.accept()

    def enter_track(self, filename):
        self.showHiddenFiles()
        self.enterManually(filename)
        self.accept()

    def select_tracks(self, of_type='mp3', *files):
        if not files:
            return
        self.view_as_list()
        self.select_files_of_type(contains_string('*.{}'.format(of_type)))
        self.showHiddenFiles()
        folder = os.path.dirname(files[0])
        self.navigateToDir(folder)
        self.selectFiles(*[os.path.basename(f) for f in files])
        self.accept()

    def rejects_selection_of(self, path):
        self.showHiddenFiles()
        self.navigateToDir(os.path.dirname(path))
        self.selectFile(os.path.basename(path))
        self.acceptButtonIs(disabled())
        self.reject()