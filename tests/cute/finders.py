# -*- coding: utf-8 -*-

from tests.cute.prober import Probe


class WidgetFinder(Probe):
    def widgets(self):
        pass


class WidgetSelector(WidgetFinder):
    def widget(self):
        pass


class RecursiveWidgetFinder(WidgetFinder):
    def __init__(self, widgetType, criteria, parentFinder):
        super(RecursiveWidgetFinder, self).__init__()
        self._widgetType = widgetType
        self._criteria = criteria
        self._parentFinder = parentFinder
        self._found = set()

    def isSatisfied(self):
        return self._parentFinder.isSatisfied()

    def widgets(self):
        return list(self._found)

    def test(self):
        self._parentFinder.test()
        self._found.clear()
        self._search(self._parentFinder.widgets())

    def describeTo(self, description):
        self._describe_briefly_to(description)
        description.append_text(" in ").append_description_of(self._parentFinder)

    def describeFailureTo(self, description):
        self._parentFinder.describeFailureTo(description)
        if self._parentFinder.isSatisfied:
            description.append_text(" contained "). \
                append_description_of(len(self._found)). \
                append_text(" ")
            self._describe_briefly_to(description)

    def _search(self, widgets):
        for widget in widgets:
            self._search_within(widget)

    def _search_within(self, widget):
        if isinstance(widget, self._widgetType) and self._criteria.matches(widget):
            self._found.add(widget)
        else:
            self._search(widget.children())

    def _describe_briefly_to(self, description):
        description.append_text(self._widgetType.__name__). \
            append_text(" "). \
            append_description_of(self._criteria)


class TopLevelFrameFinder(WidgetFinder):
    def __init__(self, app):
        super(TopLevelFrameFinder, self).__init__()
        self._app = app

    def isSatisfied(self):
        return True

    def widgets(self):
        return self._rootWindows

    def test(self):
        self._rootWindows = set()
        for topLevelWidget in self._app.topLevelWidgets():
            self._rootWindows.add(self._rootParent(topLevelWidget))

    def describeTo(self, description):
        description.append_text("top level frame")

    def describeFailureTo(self, description):
        self.describeTo(description)

    def _rootParent(self, widget):
        return widget if not widget.parent() else self._rootParent(widget.parent())


class SingleWidgetFinder(WidgetSelector):
    def __init__(self, finder):
        super(SingleWidgetFinder, self).__init__()
        self._finder = finder

    def isSatisfied(self):
        return self._finder.isSatisfied() & self._isSingle()

    def test(self):
        self._finder.test()

    def widgets(self):
        return self._finder.widgets()

    def widget(self):
        return list(self.widgets())[0]

    def describeTo(self, description):
        description.append_text("exactly 1 ").append_description_of(self._finder)

    def describeFailureTo(self, description):
        description.append_description_of(len(self.widgets())). \
            append_text(" ").append_description_of(self._finder)

    def _isSingle(self):
        return len(self.widgets()) == 1


