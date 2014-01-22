import os
import tempfile
import shutil

from hamcrest import equal_to
# noinspection PyUnresolvedReferences
import use_sip_api_v2
from PyQt4.QtGui import QMainWindow

from test.cute.probes import ValueMatcherProbe
from test.drivers.export_as_dialog_driver import exportAsDialog
from test.integration.ui.view_test import ViewTest

from tgit.ui.views.export_as_dialog import ExportAsDialog


class ExportAsDialogTest(ViewTest):
    def setUp(self):
        super(ExportAsDialogTest, self).setUp()
        self.window = QMainWindow()
        self.show(self.window)
        self.dialog = ExportAsDialog()
        self.dialog.native = False
        self.dialog.render()
        self.driver = exportAsDialog(self)
        self.exportDir = createTempDir()

    def tearDown(self):
        deleteDir(self.exportDir)
        super(ExportAsDialogTest, self).tearDown()

    def testExportsAlbumToDestinationFile(self):
        destination = os.path.join(self.exportDir, 'album.csv')
        export = ValueMatcherProbe('export as', equal_to(destination))

        class ExportListener(object):
            def exportTo(self, filename):
                export.received(filename)

        self.dialog.announceTo(ExportListener())
        self.dialog.show()
        self.driver.exportAs(destination)

        self.check(export)


def createTempDir():
    return tempfile.mkdtemp()


def deleteDir(path):
    shutil.rmtree(path)
