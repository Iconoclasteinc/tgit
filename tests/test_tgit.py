import unittest

from PyQt4.QtGui import QApplication

from tgit.tgit import TgIT

import thread

class TgitTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        QApplication.quit()

    def test_doing_nothing(self):
        self.assertTrue(True)

if __name__ == "__main__":
    app = QApplication([])
    driver = TgIT()
    driver.show()
    t = thread.start_new_thread(unittest.main, ())
    app.exec_()