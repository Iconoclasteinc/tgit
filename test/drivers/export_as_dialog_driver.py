# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QFileDialog

from cute.matchers import named
from cute.widgets import FileDialogDriver, window


def export_as_dialog(parent):
    return ExportAsDialogDriver(window(QFileDialog, named('export-as-dialog')), parent.prober, parent.gesture_performer)


class ExportAsDialogDriver(FileDialogDriver):
    def export_as(self, filename):
        self.enter_manually(filename)
        self.has_accept_button_text('&Save')
        self.accept()