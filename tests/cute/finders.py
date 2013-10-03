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
        return tuple(self._found)

    def test(self):
        self._parentFinder.test()
        self._found.clear()
        self._search(self._parentFinder.widgets())

    def describeTo(self, description):
        self._describeBrieflyTo(description)
        description.append_text("\n    in ").append_description_of(self._parentFinder)

    def describeFailureTo(self, description):
        self._parentFinder.describeFailureTo(description)
        if self._parentFinder.isSatisfied():
            description.append_text("\n    contained "). \
                append_description_of(len(self._found)). \
                append_text(" ")
            self._describeBrieflyTo(description)

    def _search(self, widgets):
        for widget in widgets:
            self._searchWithin(widget)

    def _searchWithin(self, widget):
        if isinstance(widget, self._widgetType) and self._criteria.matches(widget):
            self._found.add(widget)
        else:
            self._search(widget.findChildren(self._widgetType))

    def _describeBrieflyTo(self, description):
        description.append_text(self._widgetType.__name__). \
            append_text(" "). \
            append_description_of(self._criteria)


class TopLevelWidgetsFinder(WidgetFinder):
    def __init__(self, app):
        super(TopLevelWidgetsFinder, self).__init__()
        self._app = app

    def isSatisfied(self):
        return True

    def widgets(self):
        return tuple(self._rootWindows)

    def test(self):
        self._rootWindows = set()
        for topLevelWidget in self._app.topLevelWidgets():
            self._rootWindows.add(self._rootParent(topLevelWidget))

    def describeTo(self, description):
        description.append_text("all top level widgets")

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
        return tuple(self.widgets())[0]

    def describeTo(self, description):
        description.append_text("a unique ").append_description_of(self._finder)

    def describeFailureTo(self, description):
        self._finder.describeFailureTo(description)

    def _isSingle(self):
        return len(self.widgets()) == 1


class WidgetIdentity(WidgetSelector):
    def __init__(self, widget):
        self._widget = widget

    def test(self):
        pass

    def widgets(self):
        return self._widget,

    def widget(self):
        return self._widget

    def isSatisfied(self):
        return True

    def describeTo(self, description):
        description.append_text("the exact ") \
            .append_text(type(self._widget).__name__) \
            .append_text(" '%s'" % repr(self._widget))

    def describeFailureTo(self, description):
        self.describeTo(description)


class NthWidgetFinder(WidgetSelector):
    def __init__(self, parentFinder, index):
        super(NthWidgetFinder, self).__init__()
        self._parentFinder = parentFinder
        self._index = index

    def widgets(self):
        widgets = self._parentFinder.widgets()
        if widgets:
            return (widgets[self._index],)
        else:
            return ()

    def widget(self):
        return self.widgets()[0]

     # This expects the parent finder to describe how many were actually found.
    def describeFailureTo(self, description):
        self._parentFinder.describeFailureTo(description)
        if self.isSatisfied():
            description.append_text("\n    the ")
            description.append_value(self._index + 1)
            description.append_text("th widget")

    def describeTo(self, description):
        description.append_text("the ")
        description.append_value(self._index + 1)
        description.append_text("th widget from those matching ")
        description.append_description_of(self._parentFinder)

    def isSatisfied(self):
        return self._parentFinder.isSatisfied() and len(self._parentFinder.widgets()) > self._index

    def test(self):
        self._parentFinder.test()
