# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

MAIN_WINDOW_NAME = "TGiT"
SURPRISE_BUTTON_NAME = "surprise"


class MainWindow(object):
    def setupUi(self, window):
        window.setObjectName(_fromUtf8(MAIN_WINDOW_NAME))
        window.resize(469, 266)
        self.centralwidget = QtGui.QWidget(window)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName(_fromUtf8(SURPRISE_BUTTON_NAME))
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        window.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 469, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuQuit = QtGui.QMenu(self.menubar)
        self.menuQuit.setObjectName(_fromUtf8("menuQuit"))
        window.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(window)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        window.setStatusBar(self.statusbar)
        self.actionHit_me_to_quit = QtGui.QAction(window)
        self.actionHit_me_to_quit.setObjectName(_fromUtf8("actionHit_me_to_quit"))
        self.menuQuit.addAction(self.actionHit_me_to_quit)
        self.menubar.addAction(self.menuQuit.menuAction())

        self.retranslateUi(window)
        QtCore.QMetaObject.connectSlotsByName(window)

    def retranslateUi(self, window):
        window.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Hit me ...", None, QtGui.QApplication.UnicodeUTF8))
        self.menuQuit.setTitle(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHit_me_to_quit.setText(QtGui.QApplication.translate("MainWindow", "Hit me to quit", None, QtGui.QApplication.UnicodeUTF8))

