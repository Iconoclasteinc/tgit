# -*- coding: utf-8 -*-

from PyQt4.QtCore import QString, QRect
from PyQt4.QtGui import (QApplication, QMainWindow, QStatusBar, QWidget, QGridLayout, QPushButton,
                         QMenu, QMenuBar, QAction)

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

MAIN_WINDOW_CONTEXT = "MainWindow"
MAIN_WINDOW_NAME = "TGiT"
SURPRISE_BUTTON_NAME = "surprise"


class MainWindow(QMainWindow):
    def __init__(self, ):
        QMainWindow.__init__(self)
        self._setup_ui()

    def _setup_ui(self):
        self.setObjectName(_fromUtf8(MAIN_WINDOW_NAME))
        self.resize(469, 266)
        self.setCentralWidget(self._make_main_panel())
        self._fill_menu()
        self._make_status_bar()
        self.localize_ui()

    def _make_status_bar(self):
        self.setStatusBar(QStatusBar(self))

    def _make_main_panel(self):
        main_panel = QWidget(self)
        main_panel_layout = QGridLayout(main_panel)
        self.button = QPushButton(main_panel)
        self.button.setObjectName(_fromUtf8(SURPRISE_BUTTON_NAME))
        self.button.clicked.connect(self.print_message)
        main_panel_layout.addWidget(self.button, 0, 0, 1, 1)
        return main_panel

    def _fill_menu(self):
        menu_bar = QMenuBar(self)
        menu_bar.setGeometry(QRect(0, 0, 469, 21))
        self.quit_menu = QMenu(menu_bar)
        self.quit_menu_item = QAction(self)
        self.quit_menu_item.triggered.connect(self.close)
        self.quit_menu.addAction(self.quit_menu_item)
        self.setMenuBar(menu_bar)
        menu_bar.addAction(self.quit_menu.menuAction())

    def print_message(self):
        print "All your QT windows are belong to us !!!!"

    def localize_ui(self):
        self.setWindowTitle(QApplication.translate(MAIN_WINDOW_CONTEXT, "Main Window", None,
                                                   QApplication.UnicodeUTF8))
        self.button.setText(QApplication.translate(MAIN_WINDOW_CONTEXT, "Hit me ...", None,
                                                   QApplication.UnicodeUTF8))
        self.quit_menu.setTitle(QApplication.translate(MAIN_WINDOW_CONTEXT, "Quit", None,
                                                       QApplication.UnicodeUTF8))
        self.quit_menu_item.setText(QApplication.translate(MAIN_WINDOW_CONTEXT, "Hit me to quit",
                                                           None, QApplication.UnicodeUTF8))
