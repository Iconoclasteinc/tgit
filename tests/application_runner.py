# -*- coding: utf-8 -*-

from PyQt4.Qt import Qt, QApplication, QPushButton, QTest

from tgit.tgit import TGiT

from tgit_driver import TGiTDriver


class ApplicationRunner(object):

    def start(self):
        self.app = QApplication([])
        self.tgit = TGiT()
        self.tgit.raise_()
        self.driver = TGiTDriver(1000)

    def stop(self):
        self.driver.close()
        del self.app

    def click_on_button(self):
        main_window = self.driver.main_window()
        button = main_window.findChild(QPushButton)
        QTest.mouseMove(button, delay=100)
        QTest.mousePress(button, Qt.LeftButton, delay=100)
        QTest.mouseRelease(button, Qt.LeftButton, delay=100)
