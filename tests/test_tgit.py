import unittest

from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QPushButton
from PyQt4.QtTest import QTest

from tgit.tgit import TGiT

class TGiTTest(unittest.TestCase):

    def setUp(self):
        self.app = QApplication([])
        self.driver = TGiT()
        self.driver.show()
        QTest.qWaitForWindowShown(self.driver)

    def tearDown(self):
        self.driver.close()
        del self.app

    def test_clicking_on_button_to_demonstrate_simulating_events(self):
        button = self.driver.findChild(QPushButton)
        button.click()

if __name__ == "__main__":
    unittest.main()
