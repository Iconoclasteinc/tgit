# -*- coding: utf-8 -*-

import os
import tempfile
import shutil

from hamcrest import equal_to

from test.integration.ui.view_test import ViewTest
from PyQt4.QtGui import QMainWindow, QFileDialog
from test.cute.probes import ValueMatcherProbe
from test.cute.widgets import FileDialogDriver, window
from test.cute.matchers import named
from test.util import builders as build

from tgit.ui import constants as ui
from tgit.ui.export_as_dialog import ExportAsDialog


class ExportAsDialogTest(ViewTest):
    def setUp(self):
        super(ExportAsDialogTest, self).setUp()
        mainWindow = QMainWindow()
        self.show(mainWindow)
        self.dialog = ExportAsDialog(native=False, parent=mainWindow)
        self.driver = self.createDriver()
        self.exportDir = createTempDir()

    def tearDown(self):
        deleteDir(self.exportDir)
        super(ExportAsDialogTest, self).tearDown()

    def createDriver(self):
        return FileDialogDriver(window(QFileDialog, named(ui.EXPORT_AS_DIALOG_NAME)),
                                self.prober, self.gesturePerformer)

    def testExportsAlbumToDestinationFile(self):
        album = build.album()
        as_ = self.exportAs('album.csv')
        exportRequest = ValueMatcherProbe('export request', equal_to((album, as_)))

        class ExportRequestListener(object):
            def export(self, album, output):
                exportRequest.received((album, output))

        self.dialog.announceTo(ExportRequestListener())
        self.dialog.show(album)
        self.driver.enterManually(as_)
        self.driver.acceptButton().hasText('&Save')
        self.driver.accept()

        self.check(exportRequest)

    def exportAs(self, name):
        return os.path.join(self.exportDir, name)


def createTempDir():
    return tempfile.mkdtemp()


def deleteDir(path):
    shutil.rmtree(path)
