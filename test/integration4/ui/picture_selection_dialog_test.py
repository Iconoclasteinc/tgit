# -*- coding: utf-8 -*-

import sys
import unittest

from PyQt4.QtGui import QMainWindow

from test.drivers4.picture_selection_dialog_driver import pictureSelectionDialog
from tgit4.ui.picture_selection_dialog import PictureSelectionDialog
from test.cute4.probes import ValueMatcherProbe
from test.integration4.ui import ViewTest
from test.util4 import resources


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