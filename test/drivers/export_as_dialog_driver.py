# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QFileDialog

from cute.matchers import named
from cute.widgets import FileDialogDriver, window


def exportAsDialog(parent):
    return ExportAsDialogDriver(window(QFileDialog, named('export-as-dialog')), parent.prober, parent.gesture_performer)


class ExportAsDialogDriver(FileDialogDriver):
    def exportAs(self, filename):
        self.enter_manually(filename)
        self.accept_button_has_text('&Save')
        self.accept()