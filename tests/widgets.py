# -*- coding: utf-8 -*-

from hamcrest.core.selfdescribing import SelfDescribing
from hamcrest.core.string_description import StringDescription


def top_level_window(app):
    return SingleWidgetFinder(TopLevelWidgetsFinder(app)).widget()


class WidgetFinder(SelfDescribing):
    def widgets(self):
        pass

    def describe_failure_to(self, description):
        pass

    def description(self):
        return str(StringDescription().append_description_of(self))

    def failure_description(self):
        description = StringDescription()
        self.describe_failure_to(description)
        return str(description)


class WidgetSelector(WidgetFinder):
    def widget(self):
        pass


class TopLevelWidgetsFinder(WidgetFinder):
    def __init__(self, app):
        super(TopLevelWidgetsFinder, self).__init__()
        self.app = app

    def widgets(self):
        root_widgets = set()
        for top_level_widget in self.app.topLevelWidgets():
            root_widgets.add(self._root_parent(top_level_widget))

        return root_widgets

    def describe_to(self, description):
        description.append_text("top level widgets")

    def describe_failure_to(self, description):
        self.describe_to(description)

    def _root_parent(self, widget):
        return widget if not widget.parent() else self._root_parent(widget.parent())


class SingleWidgetFinder(WidgetSelector):
    def __init__(self, finder):
        super(SingleWidgetFinder, self).__init__()
        self.finder = finder

    def widgets(self):
        return self.finder.widgets()

    def widget(self):
        if not self._is_single():
            raise AssertionError(self.failure_description())
        return self.widgets().pop()

    def describe_to(self, description):
        description.append_text("exactly 1").append_description_of(self.finder)

    def describe_failure_to(self, description):
        description.append_value(len(self.widgets())).append_text(" ").append_description_of(self
        .finder)

    def _is_single(self):
        return len(self.widgets()) == 1

