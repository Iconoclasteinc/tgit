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
        self.exportDir = createTempDir()

    def tearDown(self):
        deleteDir(self.exportDir)
        super(ExportAsDialogTest, self).tearDown()

    def testExportsAlbumToDestinationFile(self):
        destination = os.path.join(self.exportDir, 'album.csv')
        exportAsSignal = ValueMatcherProbe('export as', equal_to(destination))

        self.dialog.bind(exportAs=exportAsSignal.received)
        self.dialog.show()
        self.driver.exportAs(destination)
        self.check(exportAsSignal)


def createTempDir():
    return tempfile.mkdtemp()


def deleteDir(path):
    shutil.rmtree(path)
