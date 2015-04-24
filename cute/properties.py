# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QObject
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QLineEdit, QDateTimeEdit, QComboBox
from hamcrest.core.selfdescribing import SelfDescribing


def name():
    return PropertyQuery('name', QObject.objectName)


def text():
    return PropertyQuery('text', lambda w: w.text())


def label_pixmap():
    return PropertyQuery('pixmap', QLabel.pixmap)


def pixmap_height():
    return PropertyQuery('pixmap height', QPixmap.height)


def pixmap_width():
    return PropertyQuery('pixmap width', QPixmap.width)


def label_buddy():
    return PropertyQuery('buddy', QLabel.buddy)


def input_text():
    return PropertyQuery('display text', QLineEdit.displayText)


def plain_text():
    return PropertyQuery('plain text', lambda w: w.toPlainText())


def current_text():
    return PropertyQuery('current text', QComboBox.currentText)


def list_item_text():
    return PropertyQuery('text', lambda item: item.data(Qt.DisplayRole))


def time():
    return PropertyQuery('time', QDateTimeEdit.time)


def title():
    return PropertyQuery('title', lambda w: w.title())


def cursor_shape():
    return PropertyQuery('cursor shape', lambda w: w.cursor().shape())


class Query(SelfDescribing):
    def __call__(self, arg):
        pass


class PropertyQuery(Query):
    def __init__(self, name, query):
        super(PropertyQuery, self).__init__()
        self._property_name = name
        self._query = query

    def __call__(self, arg):
        return self._query(arg)

    def describe_to(self, description):
        description.append_text(self._property_name)