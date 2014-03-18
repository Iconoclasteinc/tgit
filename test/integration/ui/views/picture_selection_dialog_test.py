# -*- coding: utf-8 -*-

# noinspection PyUnresolvedReferences
import use_sip_api_v2

from PyQt4.QtGui import QMainWindow

from test.drivers.picture_selection_dialog_driver import pictureSelectionDialog
from tgit.ui.views.picture_selection_dialog import PictureSelectionDialog
from test.cute.probes import ValueMatcherProbe
from test.integration.ui.views.view_test import ViewTest
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
        pictureSelected = ValueMatcherProbe('picture selected', resources.path('front-cover.jpg'))

        self.dialog.onSelectPicture(pictureSelected.received)
        self.dialog.show()
        self.driver.selectPicture(resources.path('front-cover.jpg'))

        self.check(pictureSelected)

    def testOnlyAcceptsAudioFiles(self):
        self.dialog.show()
        self.driver.rejectsSelectionOf(resources.path('base.mp3'))