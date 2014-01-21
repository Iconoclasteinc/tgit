# -*- coding: utf-8 -*-
import os
from PyQt4.QtGui import QFileDialog
from test.cute.matchers import named, disabled
from test.cute.widgets import FileDialogDriver, window
from tgit.ui.track_selection_dialog import TrackSelectionDialog


def trackSelectionDialog(parent):
    return TrackSelectionDialogDriver(
        window(QFileDialog, named(TrackSelectionDialog.NAME)), parent.prober,parent.gesturePerformer)


def folder(filename):
    return os.path.dirname(filename)


def baseName(filename):
    return os.path.basename(filename)


class TrackSelectionDialogDriver(FileDialogDriver):
    def selectTracks(self, *selection):
        if not selection:
            return
        self.showHiddenFiles()
        self.navigateToDir(folder(selection[0]))
        self.selectFiles(*[baseName(filename) for filename in selection])
        self.accept()

    def rejectsSelectionOf(self, path):
        self.showHiddenFiles()
        self.navigateToDir(folder(path))
        self.selectFile(baseName(path))
        self.acceptButtonIs(disabled())
        self.reject()