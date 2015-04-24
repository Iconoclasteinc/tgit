# -*- coding: utf-8 -*-

import os

from PyQt5.QtWidgets import QFileDialog

from cute.matchers import named, disabled
from cute.widgets import FileDialogDriver, window


def pictureSelectionDialog(parent):
    return PictureSelectionDialogDriver(
        window(QFileDialog, named('picture-selection-dialog')), parent.prober, parent.gesturePerformer)


class PictureSelectionDialogDriver(FileDialogDriver):
    def selectPicture(self, filename):
        self.view_as_list()
        self.navigateToDir(os.path.dirname(filename))
        self.selectFile(os.path.basename(filename))
        self.accept()

    def rejectsSelectionOf(self, filename):
        self.navigateToDir(os.path.dirname(filename))
        self.selectFile(os.path.basename(filename))
        self.acceptButtonIs(disabled())
        self.reject()