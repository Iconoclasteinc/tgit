# -*- coding: utf-8 -*-

from PyQt4.Qt import QObject, QLabel, QAbstractButton

from hamcrest.core.selfdescribing import SelfDescribing


def name():
    return PropertyQuery("name", QObject.objectName)


def label_text():
    return PropertyQuery("label text", QLabel.text)


def button_text():
    return PropertyQuery("button text", QAbstractButton.text)


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


