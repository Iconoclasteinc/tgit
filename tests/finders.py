# -*- coding: utf-8 -*-

from probing import Probe


class WidgetFinder(Probe):
    def widgets(self):
        pass


class WidgetSelector(WidgetFinder):
    def widget(self):
        pass


class RecursiveWidgetFinder(WidgetFinder):

    def __init__(self, widget_type, criteria, parent_or_owner_finder):
        self._widget_type = widget_type
        self._criteria = criteria
        self._parent_or_owner_finder = parent_or_owner_finder
        self._found = set()

    def is_satisfied(self):
        return self._parent_or_owner_finder.is_satisfied()

    def widgets(self):
        return list(self._found)

    def test(self):
        self._parent_or_owner_finder.test()
        self._found.clear()
        self._search(self._parent_or_owner_finder.widgets())

    def describe_to(self, description):
        self._describe_briefly_to(description)
        description.append_text(" in ").append_description_of(self._parent_or_owner_finder)

    def describe_failure_to(self, description):
        self._parent_or_owner_finder.describe_failure_to(description)
        if self._parent_or_owner_finder.is_satisfied:
            description.append_text(" contained "). \
                append_description_of(len(self._found)). \
                append_text(" ")
            self._describe_briefly_to(description)

    def _search(self, widgets):
        for widget in widgets:
            self._search_within(widget)

    def _search_within(self, widget):
        if isinstance(widget, self._widget_type) and self._criteria.matches(widget):
            self._found.add(widget)
        else:
            self._search(widget.children())

    def _describe_briefly_to(self, description):
        description.append_text(self._widget_type.__name__). \
            append_text(" "). \
            append_description_of(self._criteria)


class TopLevelWindowFinder(WidgetFinder):

    def __init__(self, app):
        super(TopLevelWindowFinder, self).__init__()
        self._app = app

    def is_satisfied(self):
        return True

    def widgets(self):
        return self.root_windows

    def test(self):
        self.root_windows = set()
        for top_level_widget in self._app.topLevelWidgets():
            self.root_windows.add(self._root_parent(top_level_widget))

    def describe_to(self, description):
        description.append_text("top level widgets")

    def describe_failure_to(self, description):
        self.describe_to(description)

    def _root_parent(self, widget):
        return widget if not widget.parent() else self._root_parent(widget.parent())


class SingleWidgetFinder(WidgetSelector):

    def __init__(self, finder):
        super(SingleWidgetFinder, self).__init__()
        self._finder = finder

    def is_satisfied(self):
        return self._finder.is_satisfied() & self._is_single()

    def test(self):
        self._finder.test()

    def widgets(self):
        return self._finder.widgets()

    def widget(self):
        return list(self.widgets())[0]

    def describe_to(self, description):
        description.append_text("exactly 1 ").append_description_of(self._finder)

    def describe_failure_to(self, description):
        description.append_description_of(len(self.widgets())). \
            append_text(" ").append_description_of(self._finder)

    def _is_single(self):
        return len(self.widgets()) == 1


