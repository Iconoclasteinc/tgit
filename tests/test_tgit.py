import unittest

from PyQt4.QtGui import QApplication

from tgit.tgit import TGiT

import thread

class TGiTTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        QApplication.quit()

    def test_doing_nothing(self):
        self.assertTrue(True)
        self.fail("Boom!")

if __name__ == "__main__":
    app = QApplication([])
    driver = TGiT()
    driver.show()
    t = thread.start_new_thread(unittest.main, ())
    app.exec_()