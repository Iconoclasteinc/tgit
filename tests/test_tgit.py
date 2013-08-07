# -*- coding: utf-8 -*-

import unittest

from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QPushButton
from PyQt4.QtTest import QTest

from tgit import tgit
import widgets


class TGiTTest(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.tgit = tgit.TGiT()
        self.driver = widgets.top_level_window(self.app)
        self.driver.show()
        self.driver.raise_()
        QTest.qWaitForWindowShown(self.driver)

    def tearDown(self):
        self.driver.close()
        del self.app

    def test_clicking_on_button_to_demonstrate_simulating_events(self):
        button = self.driver.findChild(QPushButton)
        button.click()


if __name__ == "__main__":
    unittest.main()
