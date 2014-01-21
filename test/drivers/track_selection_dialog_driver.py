# -*- coding: utf-8 -*-
from os.path import dirname, basename

from PyQt4.QtGui import QFileDialog

from test.cute.matchers import named, disabled
from test.cute.widgets import FileDialogDriver, window
from tgit.ui.views.track_selection_dialog import TrackSelectionDialog


def trackSelectionDialog(parent):
    return TrackSelectionDialogDriver(
        window(QFileDialog, named(TrackSelectionDialog.NAME)), parent.prober,parent.gesturePerformer)


class TrackSelectionDialogDriver(FileDialogDriver):
    def selectTracksInFolder(self, folder):
        self.showHiddenFiles()
        self.navigateToDir(folder)
        self.accept()

    def selectTracks(self, *files):
        if not files:
            return
        self.showHiddenFiles()
        self.navigateToDir(dirname(files[0]))
        self.selectFiles(*[basename(filename) for filename in files])
        self.accept()

    def rejectsSelectionOf(self, path):
        self.showHiddenFiles()
        self.navigateToDir(dirname(path))
        self.selectFile(basename(path))
        self.acceptButtonIs(disabled())
        self.reject()