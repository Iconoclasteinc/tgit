# -*- coding: utf-8 -*-

import os
import shutil

from hamcrest import equal_to
from PyQt5.QtWidgets import QMainWindow

from cute.probes import ValueMatcherProbe
from test.drivers import export_as_dialog
from test.integration.ui import WidgetTest
from test.util import resources
from tgit.ui.export_as_dialog import ExportAsDialog


class ExportAsDialogTest(WidgetTest):
    def setUp(self):
        super(ExportAsDialogTest, self).setUp()
        window = QMainWindow()
        self.show(window)
        self.dialog = ExportAsDialog(window, native=False, transient=False)
        self.driver = export_as_dialog(self)
        self.tempDir = resources.makeTempDir()

    def tearDown(self):
        shutil.rmtree(self.tempDir)
        super(ExportAsDialogTest, self).tearDown()

    def testSignalsExportAsDestination(self):
        destination = os.path.join(self.tempDir, 'album.csv')
        exportAsSignal = ValueMatcherProbe('export as', equal_to(destination))

        self.dialog.exportAs.connect(exportAsSignal.received)
        self.dialog.display()

        self.driver.exportAs(destination)
        self.check(exportAsSignal)