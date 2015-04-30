# -*- coding: utf-8 -*-
import os

from PyQt5.QtWidgets import QFileDialog
from hamcrest import contains_string

from cute.matchers import named, disabled, showing_on_screen
from cute.widgets import FileDialogDriver, window


def import_album_from_track_dialog(parent):
    return ImportAlbumFromTrackDialogDriver(
        window(QFileDialog, named('import_album_from_track_dialog')), parent.prober, parent.gesture_performer)


class ImportAlbumFromTrackDialogDriver(FileDialogDriver):
    def select_track(self, path, of_type='mp3'):
        self.view_as_list()
        self.show_hidden_files()
        self.filter_files_of_type(contains_string('*.{}'.format(of_type)))
        self.navigate_to_dir(os.path.dirname(path))
        self.select_file(os.path.basename(path))
        self.accept()

    def rejects_selection_of(self, path):
        self.show_hidden_files()
        self.navigate_to_dir(os.path.dirname(path))
        self.select_file(os.path.basename(path))
        self.accept_button_is(disabled())
        self.reject()