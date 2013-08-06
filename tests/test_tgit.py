# -*- coding: utf-8 -*-

import unittest

from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QPushButton
from PyQt4.QtTest import QTest

from tgit import tgit


class TGiTTest(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.tgit = tgit.TGiT()
        self.driver = self._single_widget(self._root_widgets())
        self.driver.show()
        self.driver.raise_()
        QTest.qWaitForWindowShown(self.driver)

    def tearDown(self):
        self.driver.close()
        del self.tgit
        del self.app

    def test_clicking_on_button_to_demonstrate_simulating_events(self):
        button = self.driver.findChild(QPushButton)
        button.click()

    def _root_widgets(self):
        root_widgets = set()
        for top_level_widget in self.app.topLevelWidgets():
            root_widgets.add(self._root_parent(top_level_widget))

        return root_widgets

    def _root_parent(self, widget):
        return widget if not widget.parent() else self._root_parent(widget.parent())

    def _single_widget(self, widgets):
        if len(widgets) != 1: self.fail(
            "Expected exactly 1 top level window, but got " + str(len(widgets)))
        return widgets.pop()


if __name__ == "__main__":
    unittest.main()
