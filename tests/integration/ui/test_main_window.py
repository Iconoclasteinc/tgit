# -*- coding: utf-8 -*-

import unittest

import use_sip_api_v2
from PyQt4.Qt import QApplication

from tgit.ui.main_window import MainWindow
from tests.endtoend.tgit_driver import TGiTDriver


class MainWindowTest(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.mainWindow = MainWindow()
        self.driver = TGiTDriver(100)

    def tearDown(self):
        self.driver.close()
        del self.app

    def testShowingAndClosingMainWindow(self):
        pass
