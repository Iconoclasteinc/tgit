# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QFileDialog

from cute.matchers import named
from cute.widgets import FileDialogDriver, window


def exportAsDialog(parent):
    return ExportAsDialogDriver(window(QFileDialog, named('export-as-dialog')), parent.prober, parent.gesturePerformer)


class ExportAsDialogDriver(FileDialogDriver):
    def exportAs(self, filename):
        self.enterManually(filename)
        self.acceptButtonHasText('&Save')
        self.accept()