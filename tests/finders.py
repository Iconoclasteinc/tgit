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
        self.widget_type = widget_type
        self.criteria = criteria
        self.parent_or_owner_finder = parent_or_owner_finder
        self.found = set()

    def is_satisfied(self):
        return self.parent_or_owner_finder.is_satisfied()

    def widgets(self):
        return list(self.found)

    def test(self):
        self.parent_or_owner_finder.test()
        self.found.clear()
        self._search(self.parent_or_owner_finder.widgets())

    def describe_to(self, description):
        self._describe_briefly_to(description)
        description.append_text(" in ").append_description_of(self.parent_or_owner_finder)

    def describe_failure_to(self, description):
        self.parent_or_owner_finder.describe_failure_to(description)
        if self.parent_or_owner_finder.is_satisfied:
            description.append_text(" contained "). \
                append_description_of(len(self.found)). \
                append_text(" ")
            self._describe_briefly_to(description)

    def _search(self, widgets):
        for widget in widgets:
            self._search_within(widget)

    def _search_within(self, widget):
        if isinstance(widget, self.widget_type) and self.criteria.matches(widget):
            self.found.add(widget)
        else:
            self._search(widget.children())

    def _describe_briefly_to(self, description):
        description.append_text(self.widget_type.__name__). \
            append_text(" "). \
            append_description_of(self.criteria)


class TopLevelWindowFinder(WidgetFinder):

    def __init__(self, app):
        super(TopLevelWindowFinder, self).__init__()
        self.app = app

    def is_satisfied(self):
        return True

    def widgets(self):
        return self.root_windows

    def test(self):
        self.root_windows = set()
        for top_level_widget in self.app.topLevelWidgets():
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
        self.finder = finder

    def is_satisfied(self):
        return self.finder.is_satisfied() & self._is_single()

    def test(self):
        self.finder.test()

    def widgets(self):
        return self.finder.widgets()

    def widget(self):
        return list(self.widgets())[0]

    def describe_to(self, description):
        description.append_text("exactly 1 ").append_description_of(self.finder)

    def describe_failure_to(self, description):
        description.append_description_of(len(self.widgets())). \
            append_text(" ").append_description_of(self.finder)

    def _is_single(self):
        return len(self.widgets()) == 1


