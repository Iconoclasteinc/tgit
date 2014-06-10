import os
import tempfile
import shutil

from hamcrest import equal_to

from PyQt4.QtGui import QMainWindow

from test.cute.probes import ValueMatcherProbe
from test.drivers.export_as_dialog_driver import exportAsDialog
from test.integration.ui.views import ViewTest

from tgit.ui.views.export_as_dialog import ExportAsDialog


class ExportAsDialogTest(ViewTest):
    def setUp(self):
        super(ExportAsDialogTest, self).setUp()
        self.window = QMainWindow()
        self.show(self.window)
        ExportAsDialog.native = False
        self.dialog = ExportAsDialog()
        self.driver = exportAsDialog(self)
        self.tempDir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tempDir)
        super(ExportAsDialogTest, self).tearDown()

    def testSignalsExportAsDestination(self):
        destination = os.path.join(self.tempDir, 'album.csv')
        exportAsSignal = ValueMatcherProbe('export as', equal_to(destination))

        self.dialog.select(exportAsSignal.received)
        self.driver.exportAs(destination)
        self.check(exportAsSignal)