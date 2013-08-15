# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtGui

from ui.main_window import MainWindow


class TGiT(QtGui.QApplication):
    def __init__(self):
        QtGui.QApplication.__init__(self, [])
        self.ui = MainWindow()
        self.ui.show()
        self.ui.raise_()

    def run(self):
        return sys.exit(self.exec_())


def main():
    TGiT().run()
