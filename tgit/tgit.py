# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSlot

import ui.main


class TGiT(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = ui.main.MainWindow()
        self.ui.setupUi(self)
        self.show()

    @pyqtSlot()
    def on_pushButton_clicked(self):
        print "All your QT windows are belong to us !!!!"

    @pyqtSlot()
    def on_actionHit_me_to_quit_triggered(self):
        self.close()


def main():
    app = QtGui.QApplication(sys.argv)
    TGiT()
    sys.exit(app.exec_())
