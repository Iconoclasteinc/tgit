# -*- coding: utf-8 -*-
from PyQt4.QtGui import QFileDialog
from test.cute.matchers import named
from test.cute.widgets import FileDialogDriver, window
from tgit.ui.views.export_as_dialog import ExportAsDialog


def exportAsDialog(parent):
    return ExportAsDialogDriver(window(QFileDialog, named(ExportAsDialog.NAME)), parent.prober, parent.gesturePerformer)


class ExportAsDialogDriver(FileDialogDriver):
    def exportAs(self, filename):
        self.enterManually(filename)
        self.acceptButtonHasText('&Save')
        self.accept()