# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/test.ui'
#
# Created: Sat Nov  5 13:12:38 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class MainWindow(object):
    def setupUi(self, window):
        window.setObjectName("MainWindow")
        window.resize(469, 266)
        self.centralwidget = QtWidgets.QWidget(window)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 469, 21))
        self.menubar.setObjectName("menubar")
        self.menuQuit = QtWidgets.QMenu(self.menubar)
        self.menuQuit.setObjectName("menuQuit")
        window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(window)
        self.statusbar.setObjectName("statusbar")
        window.setStatusBar(self.statusbar)
        self.actionHit_me_to_quit = QtWidgets.QAction(window)
        self.actionHit_me_to_quit.setObjectName("actionHit_me_to_quit")
        self.menuQuit.addAction(self.actionHit_me_to_quit)
        self.menubar.addAction(self.menuQuit.menuAction())

        self.retranslateUi(window)
        QtCore.QMetaObject.connectSlotsByName(window)

    def retranslateUi(self, window):
        window.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None))
        self.pushButton.setText(QtWidgets.QApplication.translate("MainWindow", "Hit me ...", None))
        self.menuQuit.setTitle(QtWidgets.QApplication.translate("MainWindow", "Quit", None))
        self.actionHit_me_to_quit.setText(QtWidgets.QApplication.translate("MainWindow", "Hit me to quit", None))

