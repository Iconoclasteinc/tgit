# -*- coding: utf-8 -*-
from os.path import dirname, basename

from PyQt4.QtGui import QFileDialog

from test.cute.matchers import named, disabled
from test.cute.widgets import FileDialogDriver, window


def trackSelectionDialog(parent):
    return TrackSelectionDialogDriver(
        window(QFileDialog, named('track-selection-dialog')), parent.prober, parent.gesturePerformer)


class TrackSelectionDialogDriver(FileDialogDriver):
    def selectTracksInFolder(self, folder):
        self.showHiddenFiles()
        self.navigateToDir(folder)
        self.accept()

    def selectTracks(self, *files):
        if not files:
            return
        self.showHiddenFiles()
        folder = dirname(files[0])
        self.navigateToDir(folder)
        self.selectFiles(*[basename(f) for f in files])
        self.accept()

    def rejectsSelectionOf(self, path):
        self.showHiddenFiles()
        self.navigateToDir(dirname(path))
        self.selectFile(basename(path))
        self.acceptButtonIs(disabled())
        self.reject()