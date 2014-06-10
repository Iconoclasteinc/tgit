# -*- coding: utf-8 -*-

from PyQt4.QtGui import QMainWindow

from test.drivers.picture_selection_dialog_driver import pictureSelectionDialog
from tgit.ui.views.picture_selection_dialog import PictureSelectionDialog
from test.cute.probes import ValueMatcherProbe
from test.integration.ui.views import ViewTest
from test.util import resources


class PictureSelectionDialogTest(ViewTest):
    def setUp(self):
        super(PictureSelectionDialogTest, self).setUp()
        self.window = QMainWindow()
        self.show(self.window)
        PictureSelectionDialog.native = False
        self.dialog = PictureSelectionDialog()
        self.driver = pictureSelectionDialog(self)

    def testSignalsWhenPictureSelected(self):
        pictureSelectedSignal = ValueMatcherProbe('picture selected', resources.path('front-cover.jpg'))

        self.dialog.select(pictureSelectedSignal.received)
        self.driver.selectPicture(resources.path('front-cover.jpg'))

        self.check(pictureSelectedSignal)

    def testOnlyAcceptsAudioFiles(self):
        def dummyHandler(selection):
            pass
        self.dialog.select(dummyHandler)
        self.driver.rejectsSelectionOf(resources.path('base.mp3'))