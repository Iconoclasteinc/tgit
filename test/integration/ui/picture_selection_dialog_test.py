# -*- coding: utf-8 -*-

import sys
import unittest

from PyQt5.QtWidgets import QMainWindow

from cute.probes import ValueMatcherProbe
from test.drivers.picture_selection_dialog_driver import pictureSelectionDialog
from test.integration.ui import WidgetTest
from test.util import resources
from tgit.ui.picture_selection_dialog import PictureSelectionDialog


class PictureSelectionDialogTest(WidgetTest):
    def setUp(self):
        super(PictureSelectionDialogTest, self).setUp()
        window = QMainWindow()
        self.show(window)
        self.dialog = PictureSelectionDialog(window, native=False, transient=False)
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