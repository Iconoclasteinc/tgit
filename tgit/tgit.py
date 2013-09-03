# -*- coding: utf-8 -*-

import sys

from PyQt4.Qt import QApplication

from ui.main_window import MainWindow


class TGiT(QApplication):
    def __init__(self):
        QApplication.__init__(self, [])
        self.ui = MainWindow()
        self._show_ui()

    def _show_ui(self):
        self.ui.show()
        self.ui.raise_()

    def run(self):
        return sys.exit(self.exec_())


def main():
    TGiT().run()
