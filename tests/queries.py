# -*- coding: utf-8 -*-

from hamcrest.core.selfdescribing import SelfDescribing


def name():
    return PropertyQuery("name", lambda widget: widget.objectName())


class Query(SelfDescribing):

    def __call__(self, arg):
        pass


class PropertyQuery(Query):

    def __init__(self, name, query):
        self._property_name = name
        self._query = query

    def __call__(self, arg):
        return self._query(arg)

    def describe_to(self, description):
        description.append_text(self._property_name)


