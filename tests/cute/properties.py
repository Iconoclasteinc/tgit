# -*- coding: utf-8 -*-

from PyQt4.Qt import Qt, QObject, QLabel, QLineEdit, QAbstractButton, QPixmap

from hamcrest.core.selfdescribing import SelfDescribing


def name():
    return PropertyQuery("name", QObject.objectName)


def labelText():
    return PropertyQuery("text", QLabel.text)


def labelPixmap():
    return PropertyQuery("pixmap", QLabel.pixmap)


def pixmapHeight():
    return PropertyQuery("pixmap height", QPixmap.height)


def pixmapWidth():
    return PropertyQuery("pixmap width", QPixmap.width)


def buddy():
    return PropertyQuery("buddy", QLabel.buddy)


def inputText():
    return PropertyQuery("text", QLineEdit.displayText)


def buttonText():
    return PropertyQuery("text", QAbstractButton.text)


def listItemText():
    return PropertyQuery("text", lambda item: item.data(Qt.DisplayRole))


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


