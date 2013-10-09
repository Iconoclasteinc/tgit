# -*- coding: utf-8 -*-

from PyQt4.QtCore import QDir, QPoint
from PyQt4.QtGui import (QApplication, QMainWindow, QLineEdit, QPushButton, QListView,
                         QToolButton, QFileDialog, QMenu, QAction)
from hamcrest import all_of, equal_to
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher

from test.cute.probes import (WidgetManipulatorProbe, WidgetAssertionProbe,
                              WidgetPropertyAssertionProbe, WidgetScreenBoundsProbe)
from test.cute.finders import (SingleWidgetFinder, TopLevelWidgetsFinder, RecursiveWidgetFinder,
                               NthWidgetFinder, WidgetSelector)
from test.cute import properties, gestures, keyboard_shortcuts as shortcuts, matchers as match


def allTopLevelWidgets():
    return TopLevelWidgetsFinder(QApplication.instance())


def onlyWidget(ofType, matching):
    return SingleWidgetFinder(RecursiveWidgetFinder(ofType, matching, allTopLevelWidgets()))


def mainWindow(*matchers):
    return onlyWidget(QMainWindow, all_of(*matchers))


class WidgetDriver(object):
    def __init__(self, selector, prober, gesturePerformer):
        self._selector = selector
        self._prober = prober
        self._gesturePerformer = gesturePerformer

    @property
    def selector(self):
        return self._selector

    @property
    def prober(self):
        return self._prober

    @property
    def gesturePerformer(self):
        return self._gesturePerformer

    @classmethod
    def findIn(cls, parent, widgetType, *matchers):
        return cls(SingleWidgetFinder(
            RecursiveWidgetFinder(widgetType, all_of(*matchers), parent.selector)),
                   parent.prober, parent.gesturePerformer)

    @classmethod
    def nthIn(cls, parent, widgetType, index, *matchers):
        return cls(NthWidgetFinder(
            RecursiveWidgetFinder(widgetType, all_of(*matchers), parent.selector), index),
                   parent.prober, parent.gesturePerformer)

    def isShowingOnScreen(self):
        self.is_(match.showingOnScreen())

    def isHidden(self):
        self.is_(match.hidden())

    def isEnabled(self):
        self.is_(match.enabled())

    def isDisabled(self):
        self.is_(match.disabled())

    def is_(self, criteria):
        self.check(WidgetAssertionProbe(self.selector, criteria))

    def has(self, query, criteria):
        self.check(WidgetPropertyAssertionProbe(self.selector, query, criteria))

    def manipulate(self, description, manipulation):
        self.check(WidgetManipulatorProbe(self.selector, manipulation, description))

    def widgetCenter(self):
        probe = WidgetScreenBoundsProbe(self.selector)
        self.check(probe)
        return probe.bounds.center()

    def click(self):
        return self.leftClickOnWidget()

    def leftClickOnWidget(self):
        self.isShowingOnScreen()
        self.perform(gestures.clickAt(self.widgetCenter()))

    def perform(self, *gestures):
        self.gesturePerformer.perform(*gestures)

    def check(self, probe):
        self.prober.check(probe)

    def close(self):
        self.manipulate("close", lambda widget: widget.close())


class MainWindowDriver(WidgetDriver):
    pass


class AbstractButtonDriver(WidgetDriver):
    def isUp(self):
        self.is_(match.unchecked())

    def isDown(self):
        self.is_(match.checked())


class LabelDriver(WidgetDriver):
    def hasText(self, matcher):
        self.has(properties.text(), wrap_matcher(matcher))

    def hasPixmap(self, matcher):
        self.has(properties.labelPixmap(), matcher)


class LineEditDriver(WidgetDriver):
    EDITION_DELAY = 20

    def hasText(self, text):
        self.has(properties.inputText(), equal_to(text))

    def replaceAllText(self, text):
        self.focusWithMouse()
        self.clearAllText()
        self.type(text)

    def focusWithMouse(self):
        self.leftClickOnWidget()

    def clearAllText(self):
        self.selectAllText()
        self.perform(gestures.pause(LineEditDriver.EDITION_DELAY))
        self.deleteSelectedText()

    def selectAllText(self):
        self.perform(shortcuts.SelectAll)

    def deleteSelectedText(self):
        self.perform(shortcuts.DeletePrevious)

    def type(self, text):
        self.perform(gestures.typeText(text))


class FileDialogDriver(WidgetDriver):
    NAVIGATION_DELAY = 20

    def showHiddenFiles(self):
        class ShowHiddenFiles(object):
            def __call__(self, dialog):
                dialog.setFilter(dialog.filter() | QDir.Hidden)

        self.manipulate("show hidden files", ShowHiddenFiles())

    def navigateToDir(self, path):
        for folderName in self._navigationPathTo(path):
            if folderName == '':
                pass
            elif folderName == '..':
                self.upOneFolder()
            else:
                self.intoFolder(folderName)

    def _navigationPathTo(self, path):
        return self._currentDir().relativeFilePath(path).split("/")

    def _currentDir(self):
        class FindOutCurrentFolder(object):
            def __call__(self, dialog):
                self.name = dialog.directory()

        currentFolder = FindOutCurrentFolder()
        self.manipulate("find out current folder", currentFolder)
        return currentFolder.name

    def intoFolder(self, name):
        self.perform(gestures.pause(FileDialogDriver.NAVIGATION_DELAY))
        self.selectFile(name)
        self._doubleClickOnFolder()
        self.perform(gestures.pause(FileDialogDriver.NAVIGATION_DELAY))

    def _doubleClickOnFolder(self):
        self.perform(gestures.mouseDoubleClick())

    def selectFile(self, name):
        self._listView().selectItem(match.withListItemText(name))

    def upOneFolder(self):
        self._toolButtonNamed('toParentButton').click()

    def _toolButtonNamed(self, name):
        return AbstractButtonDriver.findIn(self, QToolButton, match.named(name))

    def enterManually(self, filename):
        self._filenameEdit().replaceAllText(filename)

    def accept(self):
        self._acceptButton().click()

    def _listView(self):
        return ListViewDriver.findIn(self, QListView, match.named('listView'))

    def _filenameEdit(self):
        return LineEditDriver.findIn(self, QLineEdit, match.named("fileNameEdit"))

    def _acceptButton(self):
        class FindOutAcceptButtonText(object):
            def __call__(self, dialog):
                self.text = dialog.labelText(QFileDialog.Accept)

        acceptButton = FindOutAcceptButtonText()
        self.manipulate("find out accept button text", acceptButton)
        return AbstractButtonDriver.findIn(self, QPushButton, match.withText(acceptButton.text))


class ListViewDriver(WidgetDriver):
    def selectItem(self, matching):
        self._selectItem(self._indexOfFirstItem(matching))

    def _selectItem(self, index):
        self._scrollItemToVisible(index)
        self.perform(gestures.clickAt(self._centerOfItem(index)))

    def _scrollItemToVisible(self, index):
        self.manipulate("scroll item to visible", lambda listView: listView.scrollTo(index))

    def _centerOfItem(self, index):
        class CalculateCenterOfItem(object):
            def __call__(self, listView):
                itemVisibleArea = listView.visualRect(index)
                self.pos = listView.mapToGlobal(itemVisibleArea.center())

        centerOfItem = CalculateCenterOfItem()
        self.manipulate("calculate center of item", centerOfItem)
        return centerOfItem.pos

    def _indexOfFirstItem(self, matching):
        class ContainingItem(BaseMatcher):
            def __init__(self, matcher):
                super(ContainingItem, self).__init__()
                self._itemMatcher = matcher
                self.foundAtIndex = None

            def _matches(self, listView):
                model = listView.model()
                root = listView.rootIndex()
                itemCount = model.rowCount(root)
                for i in range(itemCount):
                    index = model.index(i, 0, root)
                    if self._itemMatcher.matches(index):
                        self.atIndex = index
                        return True

                return False

            def describe_to(self, description):
                description.append_text("containing an item ")
                self._itemMatcher.describe_to(description)

            def describe_mismatch(self, item, mismatch_description):
                mismatch_description.append_text("contained no item ")
                self._itemMatcher.describe_to(mismatch_description)

        containingItem = ContainingItem(matching)
        self.is_(containingItem)
        return containingItem.atIndex


class MenuBarDriver(WidgetDriver):
    def menu(self, matching):
        # We have to make sure the menu actually exists on the menu bar
        # Checking that the menu is a child of the menu bar is not sufficient
        self.hasMenu(matching)
        return MenuDriver.findIn(self, QMenu, matching)

    def hasMenu(self, matching):
        class ContainingMenu(BaseMatcher):
            def __init__(self, matcher):
                super(ContainingMenu, self).__init__()
                self._matcher = matcher

            def _matches(self, menuBar):
                for menu in [action.menu() for action in menuBar.actions()]:
                    if self._matcher.matches(menu):
                        return True
                return False

            def describe_to(self, description):
                description.append_text('containing a menu ')
                self._matcher.describe_to(description)

            def describe_mismatch(self, item, mismatch_description):
                mismatch_description.append_text("contained no menu ")
                self._matcher.describe_to(mismatch_description)

        self.is_(ContainingMenu(matching))


class MenuDriver(WidgetDriver):
    def open(self):
        # QMenuBar on Mac OS X is a wrapper for using the system-wide menu bar
        # so we cannot just click on it, we have to pop it up manually
        def popup(menu):
            menuBar = menu.parent()
            menuTitleVisibleArea = menuBar.actionGeometry(menu.menuAction())
            # We try to pop up the menu at a position that makes sense on all platforms
            # i.e. just below the menu title
            menu.popup(menuBar.mapToGlobal(menuTitleVisibleArea.bottomLeft()))

        self.manipulate("open", popup)

    def selectMenuItem(self, matching):
        # We have to make sure the item menu actually exists in the menu
        # Checking that the item is a child of the menu is not sufficient
        self.hasMenuItem(matching)
        menuItem = MenuItemDriver.findIn(self, QAction, matching)
        menuItem.click()

    def hasMenuItem(self, matching):
        class ContainingMenuItem(BaseMatcher):
            def __init__(self, matcher):
                super(ContainingMenuItem, self).__init__()
                self._matcher = matcher
                self.action = None

            def _matches(self, menu):
                for action in menu.actions():
                    if self._matcher.matches(action):
                        self.action = action
                        return True
                return False

            def describe_to(self, description):
                description.append_text('containing an item ')
                self._matcher.describe_to(description)

            def describe_mismatch(self, item, mismatch_description):
                mismatch_description.append_text("contained no item ")
                self._matcher.describe_to(mismatch_description)

        containingMenuItem = ContainingMenuItem(matching)
        self.is_(containingMenuItem)
        return containingMenuItem.action


class MenuItemDriver(WidgetDriver):
    def _centerOfItem(self):
        class CalculateCenterOfItem(object):
            def __call__(self, item):
                menu = item.parent()
                itemVisibleArea = menu.actionGeometry(item)
                self.coordinates = menu.mapToGlobal(itemVisibleArea.center())

        center = CalculateCenterOfItem()
        self.manipulate("calculate center of item", center)
        return center.coordinates

    def click(self):
        self.perform(gestures.mouseMove(self._centerOfItem()), gestures.mouseClick())


class TableDriver(WidgetDriver):
    def hasHeading(self, matching):
        class ContainingHeaders(BaseMatcher):
            def __init__(self, matcher):
                super(ContainingHeaders, self).__init__()
                self._matcher = matcher

            def _headersOf(self, table):
                return [table.horizontalHeaderItem(column)
                        for column in xrange(table.columnCount())]

            def _matches(self, table):
                return self._matcher.matches(self._headersOf(table))

            def describe_to(self, description):
                description.append_text('with headers ')
                self._matcher.describe_to(description)

            def describe_mismatch(self, table, mismatch_description):
                mismatch_description.append_text("headers ")
                self._matcher.describe_mismatch(self._headersOf(table), mismatch_description)

        self.is_(ContainingHeaders(matching))

    def hasRow(self, matching):
        class ContainingCells(BaseMatcher):
            def __init__(self, matcher):
                super(ContainingCells, self).__init__()
                self._matcher = matcher

            def _cellsOf(self, table, row):
                return [table.item(row, column) for column in xrange(table.columnCount())]

            def _matches(self, table):
                for row in xrange(table.rowCount()):
                    if self._matcher.matches(self._cellsOf(table, row)):
                        self.inRow = row
                        return True
                return False

            def describe_to(self, description):
                description.append_text('containing row ')
                self._matcher.describe_to(description)

            def describe_mismatch(self, table, mismatch_description):
                mismatch_description.append_text("contained no row ")
                self._matcher.describe_to(mismatch_description)

        containingCells = ContainingCells(matching)
        self.is_(containingCells)
        return containingCells.inRow

    def scrollCellToVisible(self, column, row):
        class ScrollCellToVisible(object):
            def __init__(self, row, column):
                self._row = row
                self._column = column

            def __call__(self, table):
                table.scrollTo(table.indexAt(QPoint(table.columnViewportPosition(self._column),
                                                    table.rowViewportPosition(self._row))))

        scrollCellToVisible = ScrollCellToVisible(row, column)
        self.manipulate("scroll cell (%s, %s) into view" % (row, column), scrollCellToVisible)

    def _clickAt(self, column, row):
        class CalculateCellPosition(object):
            def __init__(self, row, column):
                self._row = row
                self._column = column

            def centerOfCell(self, table):
                rowOffset = table.horizontalHeader().height() + \
                            table.rowViewportPosition(self._row)
                columnOffset = table.verticalHeader().width() + \
                               table.columnViewportPosition(self._column)
                return QPoint(columnOffset + table.columnWidth(column) / 2,
                              rowOffset + table.rowHeight(row) / 2)

            def __call__(self, table):
                self.center = table.mapToGlobal(self.centerOfCell(table))

        cellPosition = CalculateCellPosition(row, column)
        self.manipulate("calculate cell (%s, %s) center position % (row, column)", cellPosition)
        self.perform(gestures.clickAt(cellPosition.center))

    def clickOnCell(self, row, column):
        self.scrollCellToVisible(column, row)
        self._clickAt(column, row)

    def widgetInCell(self, row, column):
        class WidgetAt(WidgetSelector):
            def __init__(self, tableSelector, row, column):
                super(WidgetAt, self).__init__()
                self._tableSelector = tableSelector
                self._row = row
                self._column = column

            def describeTo(self, description):
                description.append_text("in cell (%s, %s) widget" % (self._row, self._column))
                description.append_text("\n    in ")
                description.append_description_of(self._tableSelector)

            def describeFailureTo(self, description):
                self._tableSelector.describeFailureTo(description)
                if self._tableSelector.isSatisfied():
                    if self.isSatisfied():
                        description.append_text("\n    cell (%s, %s)" % (self._row, self._column))
                    else:
                        description.append_text("\n    had no widget in cell (%s, %s) "
                                                % (self._row, self._column))

            def widgets(self):
                if self.isSatisfied():
                    return self._cellWidget,
                else:
                    return ()

            def isSatisfied(self):
                return self._cellWidget is not None

            def test(self):
                self._tableSelector.test()

                if not self._tableSelector.isSatisfied():
                    self._cellWidget = None
                    return

                table = self._tableSelector.widget()
                self._cellWidget = table.cellWidget(self._row, self._column)

        return WidgetDriver(WidgetAt(self.selector, row, column), self.prober,
                            self.gesturePerformer)

    def hasRowCount(self, matching):
        self.is_(match.withRowCount(matching))
