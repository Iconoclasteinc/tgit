# -*- coding: utf-8 -*-

import os

from PyQt4.QtGui import QFileDialog

from test.cute4.matchers import named, disabled
from test.cute4.widgets import FileDialogDriver, window


def pictureSelectionDialog(parent):
    return PictureSelectionDialogDriver(
        window(QFileDialog, named('picture-selection-dialog')), parent.prober, parent.gesturePerformer)


class PictureSelectionDialogDriver(FileDialogDriver):
    def selectPicture(self, filename):
        self.navigateToDir(os.path.dirname(filename))
        self.selectFile(os.path.basename(filename))
        self.accept()

    def rejectsSelectionOf(self, filename):
        self.navigateToDir(os.path.dirname(filename))
        self.selectFile(os.path.basename(filename))
        self.acceptButtonIs(disabled())
        self.reject()
