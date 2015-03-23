# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QObject
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QLineEdit, QDateTimeEdit, QComboBox
from hamcrest.core.selfdescribing import SelfDescribing


def name():
    return PropertyQuery('name', QObject.objectName)


def text():
    return PropertyQuery('text', lambda w: w.text())


def labelPixmap():
    return PropertyQuery('pixmap', QLabel.pixmap)


def pixmapHeight():
    return PropertyQuery('pixmap height', QPixmap.height)


def pixmapWidth():
    return PropertyQuery('pixmap width', QPixmap.width)


def labelBuddy():
    return PropertyQuery('buddy', QLabel.buddy)


def inputText():
    return PropertyQuery('display text', QLineEdit.displayText)


def plainText():
    return PropertyQuery('plain text', lambda w: w.toPlainText())


def currentText():
    return PropertyQuery('current text', QComboBox.currentText)


def listItemText():
    return PropertyQuery('text', lambda item: item.data(Qt.DisplayRole))


def time():
    return PropertyQuery('time', QDateTimeEdit.time)


def title():
    return PropertyQuery('title', lambda w: w.title())


def cursorShape():
    return PropertyQuery('cursor shape', lambda w: w.cursor().shape())


class Query(SelfDescribing):
    def __call__(self, arg):
        pass


class PropertyQuery(Query):
    def __init__(self, name, query):
        super(PropertyQuery, self).__init__()
        self._propertyName = name
        self._query = query

    def __call__(self, arg):
        return self._query(arg)

    def describe_to(self, description):
        description.append_text(self._propertyName)