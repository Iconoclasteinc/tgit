# -*- coding: utf-8 -*-
import os

from PyQt5.QtWidgets import QFileDialog

from cute import platforms
from cute.matchers import disabled
from cute.widgets import QFileDialogDriver, window


def file_selection_dialog(parent):
    return FileDialogDriver(window(QFileDialog), parent.prober, parent.gesture_performer)


class FileDialogDriver(QFileDialogDriver):
    # We need this pause to allow system events to reach the Qt event loop before the next selection
    # Do not remove
    FILE_LIST_DISPLAY_DELAY = 40 if platforms.windows or platforms.linux else 0

    def navigate_to_dir(self, path):
        self.view_as_list()
        self.show_hidden_files()

        for folder_name in self._navigation_path_to(path):
            if folder_name == "":
                pass
            elif folder_name == "..":
                self.up_one_folder()
                self.pause(self.FILE_LIST_DISPLAY_DELAY)
                self.refresh()
            else:
                self.into_folder(folder_name)
                self.pause(self.FILE_LIST_DISPLAY_DELAY)
                self.refresh()

    def _navigation_path_to(self, path):
        return self.current_dir.relativeFilePath(path).split('/')

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
