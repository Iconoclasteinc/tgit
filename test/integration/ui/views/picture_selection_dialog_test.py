# -*- coding: utf-8 -*-

# noinspection PyUnresolvedReferences
import use_sip_api_v2

from PyQt4.QtGui import QMainWindow

from test.drivers.picture_selection_dialog_driver import pictureSelectionDialog
from tgit.ui.views import PictureSelectionDialog
from test.cute.probes import ValueMatcherProbe
from test.integration.ui.view_test import ViewTest
from test.util import resources


class PictureSelectionDialogTest(ViewTest):
    def setUp(self):
        super(PictureSelectionDialogTest, self).setUp()
        self.window = QMainWindow()
        self.show(self.window)
        self.dialog = PictureSelectionDialog()
        self.dialog.native = False
        self.driver = pictureSelectionDialog(self)

    def testSignalsWhenPictureSelected(self):
        pictureSelected = ValueMatcherProbe('picture selected', resources.path('front-cover.jpg'))

        class SelectionListener(object):
            def pictureSelected(self, filename):
                pictureSelected.received(filename)

        self.dialog.announceTo(SelectionListener())
        self.dialog.render()
        self.driver.selectPicture(resources.path('front-cover.jpg'))

        self.check(pictureSelected)

    def testOnlyAcceptsAudioFiles(self):
        self.dialog.render()
        self.driver.rejectsSelectionOf(resources.path('base.mp3'))