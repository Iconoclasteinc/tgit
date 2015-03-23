import os
import shutil

from hamcrest import equal_to
from PyQt4.QtGui import QMainWindow

from test.cute4.probes import ValueMatcherProbe
from test.drivers4.export_as_dialog_driver import exportAsDialog
from test.integration4.ui import ViewTest
from test.util4 import resources

from tgit4.ui.export_as_dialog import ExportAsDialog


class ExportAsDialogTest(ViewTest):
    def setUp(self):
        super(ExportAsDialogTest, self).setUp()
        window = QMainWindow()
        self.show(window)
        self.dialog = ExportAsDialog(window, native=False)
        self.driver = exportAsDialog(self)
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