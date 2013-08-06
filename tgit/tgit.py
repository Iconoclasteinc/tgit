#!/usr/bin/env python
# Mini App to test installer stuff

import sys
import tgit.tgit_ui

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot


class TGiT(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = tgit.tgit_ui.MainWindow()
        self.ui.setupUi(self)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        print("All your QT windows are belong to us !!!!")

    @pyqtSlot()
    def on_actionHit_me_to_quit_triggered(self):
        self.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    tagger = TGiT()
    tagger.show()
    sys.exit(app.exec_())
