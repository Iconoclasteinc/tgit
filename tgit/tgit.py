#!/usr/bin/env python
# Mini App to test installer stuff

import sys
import ui_tgit

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSlot


class Window(QtGui.QMainWindow, ui_tgit.Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        ui_tgit.Ui_MainWindow.__init__(self)
        self.setupUi(self)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        print "All your QT windows are belong to us !!!!"

    @pyqtSlot()
    def on_actionHit_me_to_quit_triggered(self):
        QtGui.QApplication.quit()

app = QtGui.QApplication(sys.argv)
Win = Window()
Win.show()
sys.exit(app.exec_())
