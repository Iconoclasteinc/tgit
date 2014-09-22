# -*- coding: utf-8 -*-
import unittest
from tgit.util import sip_api
sip_api.use_v2()

from PyQt4.QtGui import QMainWindow
import sys

from test.drivers.picture_selection_dialog_driver import pictureSelectionDialog
from tgit.ui.picture_selection_dialog import PictureSelectionDialog
from test.cute.probes import ValueMatcherProbe
from test.integration.ui import ViewTest
from test.util import resources


class PictureSelectionDialogTest(ViewTest):
    def setUp(self):
        super(PictureSelectionDialogTest, self).setUp()
        window = QMainWindow()
        self.show(window)
        self.dialog = PictureSelectionDialog(window, native=False)
        self.driver = pictureSelectionDialog(self)

    def testSignalsWhenPictureSelected(self):
        pictureSelectedSignal = ValueMatcherProbe('picture selected', resources.path('front-cover.jpg'))
        self.dialog.pictureSelected.connect(pictureSelectedSignal.received)

        self.dialog.display()
        self.driver.selectPicture(resources.path('front-cover.jpg'))
        self.check(pictureSelectedSignal)

    @unittest.skipIf(sys.platform.startswith("win"), "not supported on Windows")
    def testOnlyAcceptsPictureFiles(self):
        self.dialog.display()
        self.driver.rejectsSelectionOf(resources.path('base.mp3'))