import unittest

from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt

from tgit.tgit import TgIT

class TgitTest(unittest.TestCase):

    def setUp(self):
        '''Create the GUI'''
        self.app = QApplication([])
        self.driver = TgIT()
        self.driver.show()

    def test_doing_nothing(self):
        self.app.exec_()
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
