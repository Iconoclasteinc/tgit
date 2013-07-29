#!/usr/bin/env python
# Mini App to test installer stuff

import sys
import tgit_ui

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSlot


class TgIT(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        ui = tgit_ui.MainWindow()
        ui.setupUi(self)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        print "All your QT windows are belong to us !!!!"

    @pyqtSlot()
    def on_actionHit_me_to_quit_triggered(self):
        self.close()


def main():
    app = QtGui.QApplication(sys.argv)
    tagger = TgIT()
    tagger.show()
    sys.exit(app.exec_())
