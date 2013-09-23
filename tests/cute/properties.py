# -*- coding: utf-8 -*-

from PyQt4.Qt import Qt, QObject, QLabel, QLineEdit, QAbstractButton

from hamcrest.core.selfdescribing import SelfDescribing


def name():
    return PropertyQuery("name", QObject.objectName)


def labelText():
    return PropertyQuery("label text", QLabel.text)


def inputText():
    return PropertyQuery("input text", QLineEdit.displayText)


def buttonText():
    return PropertyQuery("button text", QAbstractButton.text)


def listItemText():
    return PropertyQuery("item text", lambda item: item.data(Qt.DisplayRole))


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


