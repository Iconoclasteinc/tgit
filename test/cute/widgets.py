# -*- coding: utf-8 -*-

from hamcrest import all_of, equal_to
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher

from PyQt4.QtCore import QDir, QPoint, Qt, QTime
from PyQt4.QtGui import (QApplication, QMainWindow, QLineEdit, QPushButton, QListView,
                         QToolButton, QFileDialog, QMenu, QAction)

from test.cute.probes import (WidgetManipulatorProbe, WidgetAssertionProbe,
                              WidgetPropertyAssertionProbe, WidgetScreenBoundsProbe)
from test.cute.finders import (SingleWidgetFinder, TopLevelWidgetsFinder, RecursiveWidgetFinder,
                               NthWidgetFinder, WidgetSelector)
from test.cute import properties, gestures, keyboard_shortcuts as shortcuts, matchers as match


def allTopLevelWidgets():
    return TopLevelWidgetsFinder(QApplication.instance())


def onlyWidget(ofType, matching):
    return SingleWidgetFinder(RecursiveWidgetFinder(ofType, matching, allTopLevelWidgets()))


def mainApplicationWindow(*matchers):
    return onlyWidget(QMainWindow, all_of(*matchers))


def window(ofType, *matchers):
    return onlyWidget(ofType, all_of(*matchers))


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
    def findSingle(cls, parent, widgetType, *matchers):
        return cls(SingleWidgetFinder(
            RecursiveWidgetFinder(widgetType, all_of(*matchers), parent.selector)),
            parent.prober, parent.gesturePerformer)

    @classmethod
    def findNth(cls, parent, widgetType, index, *matchers):
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

    def hasCursorShape(self, shape):
        self.has(properties.cursorShape(), wrap_matcher(shape))

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

    def enter(self):
        self.perform(shortcuts.Enter)

    def perform(self, *gestures):
        self.gesturePerformer.perform(*gestures)

    def check(self, probe):
        self.prober.check(probe)

    def close(self):
        self.manipulate('close', lambda widget: widget.close())

    def clearFocus(self):
        self.manipulate('clear focus', lambda widget: widget.clearFocus())


class MainWindowDriver(WidgetDriver):
    pass


class ButtonDriver(WidgetDriver):
    def hasText(self, matcher):
        self.has(properties.text(), wrap_matcher(matcher))

    def isUp(self):
        self.isShowingOnScreen()
        self.is_(match.unchecked())

    def isDown(self):
        self.isShowingOnScreen()
        self.is_(match.checked())


class LabelDriver(WidgetDriver):
    def hasText(self, matcher):
        self.has(properties.text(), wrap_matcher(matcher))

    def hasPixmap(self, matcher):
        self.has(properties.labelPixmap(), matcher)


class AbstractEditDriver(WidgetDriver):
    EDITION_DELAY = 20

    def changeText(self, text):
        self.replaceAllText(text)
        self.enter()

    def replaceAllText(self, text):
        self.focusWithMouse()
        self.clearAllText()
        self.type(text)

    def focusWithMouse(self):
        self.leftClickOnWidget()

    def clearAllText(self):
        self.selectAllText()
        self.perform(gestures.pause(self.EDITION_DELAY))
        self.deleteSelectedText()

    def selectAllText(self):
        self.perform(shortcuts.SelectAll)

    def deleteSelectedText(self):
        self.perform(shortcuts.DeletePrevious)

    def type(self, text):
        self.perform(gestures.typeText(text))


class LineEditDriver(AbstractEditDriver):
    def hasText(self, text):
        self.has(properties.inputText(), equal_to(text))


class TextEditDriver(AbstractEditDriver):
    def hasPlainText(self, text):
        self.has(properties.plainText(), equal_to(text))

    def addLine(self, text):
        self.focusWithMouse()
        self.type(text)
        self.perform(shortcuts.Enter)


class DateTimeEditDriver(WidgetDriver):
    def hasTime(self, time):
        class QueryDisplayFormat(object):
            def __call__(self, dateTimeEdit):
                self.result = dateTimeEdit.displayFormat()

        queryDisplayFormat = QueryDisplayFormat()
        self.manipulate('query display format', queryDisplayFormat)

        self.has(properties.time(), equal_to(QTime.fromString(time, queryDisplayFormat.result)))


class FileDialogDriver(WidgetDriver):
    NAVIGATION_DELAY = 50

    def showHiddenFiles(self):
        class ShowHiddenFiles(object):
            def __call__(self, dialog):
                dialog.setFilter(dialog.filter() | QDir.Hidden)

        self.manipulate('show hidden files', ShowHiddenFiles())

    def navigateToDir(self, path):
        for folderName in self._navigationPathTo(path):
            if folderName == '':
                pass
            elif folderName == '..':
                self.upOneFolder()
            else:
                self.intoFolder(folderName)

    def _navigationPathTo(self, path):
        return self._currentDir().relativeFilePath(path).split('/')

    def _currentDir(self):
        class FindOutCurrentFolder(object):
            def __call__(self, dialog):
                self.name = dialog.directory()

        currentFolder = FindOutCurrentFolder()
        self.manipulate('find out current folder', currentFolder)
        return currentFolder.name

    def intoFolder(self, name):
        self.perform(gestures.pause(self.NAVIGATION_DELAY))
        self.selectFile(name)
        self._doubleClickOnFolder()
        self.perform(gestures.pause(self.NAVIGATION_DELAY))

    def _doubleClickOnFolder(self):
        self.perform(gestures.mouseDoubleClick())

    def selectFile(self, name):
        self.selectFiles(name)

    def selectFiles(self, *names):
        self._listView().selectItems(*[match.withListItemText(name) for name in names])

    def upOneFolder(self):
        self._toolButtonNamed('toParentButton').click()

    def _toolButtonNamed(self, name):
        return ButtonDriver.findSingle(self, QToolButton, match.named(name))

    def enterManually(self, filename):
        self._filenameEdit().replaceAllText(filename)

    def accept(self):
        self.acceptButton().click()

    def acceptButtonIs(self, criteria):
        return self._dialogButton(QFileDialog.Accept).is_(criteria)

    def acceptButtonHasText(self, text):
        return self.acceptButton().hasText(text)

    def reject(self):
        return self.rejectButton().click()

    def rejectButtonIs(self, criteria):
        return self.rejectButton().is_(criteria)

    def rejectButtonHasText(self, text):
        return self.rejectButton().hasText(text)

    def _listView(self):
        return ListViewDriver.findSingle(self, QListView, match.named('listView'))

    def _filenameEdit(self):
        return LineEditDriver.findSingle(self, QLineEdit, match.named('fileNameEdit'))

    def acceptButton(self):
        return self._dialogButton(QFileDialog.Accept)

    def rejectButton(self):
        return self._dialogButton(QFileDialog.Reject)

    def _dialogButton(self, label):
        class QueryButtonText(object):
            def __init__(self, label):
                super(QueryButtonText, self).__init__()
                self._label = label

            def __call__(self, dialog):
                self.text = dialog.labelText(self._label)

        buttonText = QueryButtonText(label)
        self.manipulate('query button text', buttonText)
        return ButtonDriver.findSingle(self, QPushButton, match.withText(buttonText.text))


class ListViewDriver(WidgetDriver):
    def selectItems(self, *matchers):
        self._selectItems([self._indexOfFirstItem(matching) for matching in matchers])

    def _selectItems(self, indexes):
        self._selectItem(indexes.pop(0))
        for index in indexes:
            self._multiSelectItem(index)

    def _multiSelectItem(self, index):
        self._scrollItemToVisible(index)
        self.perform(
            gestures.withModifiers(Qt.ControlModifier, gestures.clickAt(self._centerOfItem(index))))

    def _selectItem(self, index):
        self._scrollItemToVisible(index)
        self.perform(gestures.clickAt(self._centerOfItem(index)))

    def _scrollItemToVisible(self, index):
        self.manipulate('scroll item to visible', lambda listView: listView.scrollTo(index))

    def _centerOfItem(self, index):
        class CalculateCenterOfItem(object):
            def __call__(self, listView):
                itemVisibleArea = listView.visualRect(index)
                self.pos = listView.mapToGlobal(itemVisibleArea.center())

        centerOfItem = CalculateCenterOfItem()
        self.manipulate('calculate center of item', centerOfItem)
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
                description.append_text('containing an item ')
                self._itemMatcher.describe_to(description)

            def describe_mismatch(self, item, mismatch_description):
                mismatch_description.append_text('contained no item ')
                self._itemMatcher.describe_to(mismatch_description)

        containingItem = ContainingItem(matching)
        self.is_(containingItem)
        return containingItem.atIndex


class QMenuBarDriver(WidgetDriver):
    def menu(self, matching):
        # We have to make sure the menu actually exists on the menu bar
        # Checking that the menu is a child of the menu bar is not sufficient
        self.hasMenu(matching)
        return MenuDriver.findSingle(self, QMenu, matching)

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
                mismatch_description.append_text('contained no menu ')
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

        self.manipulate('open', popup)

    def menuItem(self, matching):
        # We have to make sure the item menu actually exists in the menu
        # Checking that the item is a child of the menu is not sufficient
        self.hasMenuItem(matching)
        return MenuItemDriver.findSingle(self, QAction, matching)

    def selectMenuItem(self, matching):
        menuItem = self.menuItem(matching)
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
                mismatch_description.append_text('contained no item ')
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
        self.manipulate('calculate center of item', center)
        return center.coordinates

    def click(self):
        self.perform(gestures.mouseMove(self._centerOfItem()), gestures.mouseClick())


class TableViewDriver(WidgetDriver):
    def hasHeaders(self, matching):
        class WithHeaders(BaseMatcher):
            def __init__(self, matcher):
                super(WithHeaders, self).__init__()
                self._matcher = matcher

            def _headers(self, table):
                return [headerText(table, column) for column in xrange(columnCount(table))]

            def _matches(self, table):
                return self._matcher.matches(self._headers(table))

            def describe_to(self, description):
                description.append_text('with headers ')
                self._matcher.describe_to(description)

            def describe_mismatch(self, table, mismatch_description):
                mismatch_description.append_text('headers ')
                self._matcher.describe_mismatch(self._headers(table), mismatch_description)

        self.is_(WithHeaders(matching))

    def hasRow(self, matching):
        class RowInTable(BaseMatcher):
            def __init__(self, matcher):
                super(RowInTable, self).__init__()
                self._matcher = matcher

            def _cellsOf(self, table, row):
                return [cellText(table, row, column) for column in xrange(columnCount(table))]

            def _matches(self, table):
                for row in xrange(rowCount(table)):
                    if self._matcher.matches(self._cellsOf(table, row)):
                        self.inRow = visualRow(table, row)
                        return True
                return False

            def describe_to(self, description):
                description.append_text('containing row ')
                self._matcher.describe_to(description)

            def describe_mismatch(self, table, mismatch_description):
                mismatch_description.append_text('contained no row ')
                self._matcher.describe_to(mismatch_description)

        rowInTable = RowInTable(matching)
        self.is_(rowInTable)
        return rowInTable.inRow

    def containsRows(self, matching):
        class WithRows(BaseMatcher):
            def __init__(self, matcher):
                super(WithRows, self).__init__()
                self._matcher = matcher

            def _cellsIn(self, table, row):
                return [cellText(table, row, column) for column in xrange(columnCount(table))]

            def _rowsIn(self, table):
                rows = []
                for row in range(rowCount(table)):
                    rows.append(self._cellsIn(table, row))
                return rows

            def _matches(self, table):
                return self._matcher.matches(self._rowsIn(table))

            def describe_to(self, description):
                description.append_text('with rows ')
                self._matcher.describe_to(description)

            def describe_mismatch(self, table, mismatch_description):
                mismatch_description.append_text('rows ')
                self._matcher.describe_mismatch(self._rowsIn(table),
                                                mismatch_description)

        self.is_(WithRows(matching))

    def scrollCellToVisible(self, row, column):
        class ScrollCellToVisible(object):
            def __init__(self, row, column):
                self._row = row
                self._column = column

            def __call__(self, table):
                row, column = cellLocation(table, self._row, self._column)
                table.scrollTo(table.indexAt(QPoint(table.columnViewportPosition(column),
                                                    table.rowViewportPosition(row))))

        scrollCellToVisible = ScrollCellToVisible(row, column)
        self.manipulate('scroll cell (%s, %s) into view' % (row, column), scrollCellToVisible)

    def _clickAtCellCenter(self, row, column):
        class CalculateCellPosition(object):
            def __init__(self, row, column):
                self._row = row
                self._column = column

            def centerOfCell(self, table):
                row, column = cellLocation(table, self._row, self._column)
                rowOffset = table.horizontalHeader().height() + table.rowViewportPosition(row)
                columnOffset = table.verticalHeader().width() + table.columnViewportPosition(column)
                return QPoint(columnOffset + table.columnWidth(column) / 2,
                              rowOffset + table.rowHeight(row) / 2)

            def __call__(self, table):
                self.center = table.mapToGlobal(self.centerOfCell(table))

        cellPosition = CalculateCellPosition(row, column)
        self.manipulate('calculate cell (%s, %s) center position' % (row, column), cellPosition)
        self.perform(gestures.clickAt(cellPosition.center))

    def clickOnCell(self, row, column):
        self.scrollCellToVisible(row, column)
        self._clickAtCellCenter(row, column)

    def widgetInCell(self, row, column):
        class WidgetAt(WidgetSelector):
            def __init__(self, tableSelector, row, column):
                super(WidgetAt, self).__init__()
                self._tableSelector = tableSelector
                self._row = row
                self._column = column

            def describeTo(self, description):
                description.append_text('in cell (%s, %s) widget' % (self._row, self._column))
                description.append_text('\n    in ')
                description.append_description_of(self._tableSelector)

            def describeFailureTo(self, description):
                self._tableSelector.describeFailureTo(description)
                if self._tableSelector.isSatisfied():
                    if self.isSatisfied():
                        description.append_text('\n    cell (%s, %s)' % (self._row, self._column))
                    else:
                        description.append_text('\n    had no widget in cell (%s, %s)'
                                                % (self._row, self._column))

            def widgets(self):
                if self.isSatisfied():
                    return self._widgetInCell,
                else:
                    return ()

            def isSatisfied(self):
                return self._widgetInCell is not None

            def test(self):
                self._tableSelector.test()

                if not self._tableSelector.isSatisfied():
                    self._widgetInCell = None
                    return

                table = self._tableSelector.widget()
                self._widgetInCell = widgetAt(table, self._row, self._column)

        return WidgetDriver(WidgetAt(self.selector, row, column), self.prober,
                            self.gesturePerformer)

    def hasRowCount(self, matching):
        class WithRowCount(BaseMatcher):
            def __init__(self, matcher):
                super(WithRowCount, self).__init__()
                self._matcher = matcher

            def _matches(self, table):
                return self._matcher.matches(rowCount(table))

            def describe_to(self, description):
                description.append_text('with row count ')
                self._matcher.describe_to(description)

            def describe_mismatch(self, table, mismatch_description):
                mismatch_description.append_text('row count ')
                self._matcher.describe_mismatch(rowCount(table), mismatch_description)

        self.is_(WithRowCount(matching))

    def moveRow(self, oldPosition, newPosition):
        class MoveRow(object):
            def __init__(self, oldPosition, newPosition):
                self._oldPosition = oldPosition
                self._newPosition = newPosition

            def __call__(self, table):
                table.verticalHeader().moveSection(rowLocation(table, oldPosition),
                                                   rowLocation(table, newPosition))

        # We'd like to use gestures but drag and drop is not supported by our Robot
        # so we have to use a manipulation
        self.manipulate('move row %s to position %s' % (oldPosition, newPosition),
                        MoveRow(oldPosition, newPosition))


class TableWidgetDriver(TableViewDriver):
    def hasHeaderItems(self, matching):
        class WithHeaders(BaseMatcher):
            def __init__(self, matcher):
                super(WithHeaders, self).__init__()
                self._matcher = matcher

            def _headerItems(self, table):
                return [table.horizontalHeaderItem(columnLocation(table, column))
                        for column in xrange(table.columnCount())]

            def _matches(self, table):
                return self._matcher.matches(self._headerItems(table))

            def describe_to(self, description):
                description.append_text('with header items ')
                self._matcher.describe_to(description)

            def describe_mismatch(self, table, mismatch_description):
                mismatch_description.append_text('header items ')
                self._matcher.describe_mismatch(self._headerItems(table), mismatch_description)

        self.is_(WithHeaders(matching))

    def hasRowItems(self, matching):
        class RowInTable(BaseMatcher):
            def __init__(self, matcher):
                super(RowInTable, self).__init__()
                self._matcher = matcher

            def _cellItems(self, table, row):
                return [table.item(row, column) for column in xrange(table.columnCount())]

            def _matches(self, table):
                for row in xrange(table.rowCount()):
                    if self._matcher.matches(self._cellItems(table, row)):
                        self.inRow = table.visualRow(row)
                        return True
                return False

            def describe_to(self, description):
                description.append_text('containing row items ')
                self._matcher.describe_to(description)

            def describe_mismatch(self, table, mismatch_description):
                mismatch_description.append_text('contained no items ')
                self._matcher.describe_to(mismatch_description)

        rowInTable = RowInTable(matching)
        self.is_(rowInTable)
        return rowInTable.inRow

    def containsRowItems(self, matching):
        class WithRows(BaseMatcher):
            def __init__(self, matcher):
                super(WithRows, self).__init__()
                self._matcher = matcher

            def _cellItems(self, table, row):
                return [table.item(row, column) for column in xrange(table.columnCount())]

            def _rowsItems(self, table):
                rows = []
                for row in xrange(table.rowCount()):
                    rows.append(self._cellItems(table, row))
                return rows

            def _matches(self, table):
                return self._matcher.matches(self._rowsItems(table))

            def describe_to(self, description):
                description.append_text('with row items ')
                self._matcher.describe_to(description)

            def describe_mismatch(self, table, mismatch_description):
                mismatch_description.append_text('row items ')
                self._matcher.describe_mismatch(self._rowsItems(table), mismatch_description)

        self.is_(WithRows(matching))


def columnLocation(table, column):
    return table.horizontalHeader().logicalIndex(column)


def rowLocation(table, row):
    return table.verticalHeader().logicalIndex(row)


def cellLocation(table, row, column):
    return rowLocation(table, row), columnLocation(table, column)


def cellText(table, row, column):
    return table.model().data(table.model().index(row, column), Qt.DisplayRole)


def headerText(table, column):
    return table.model().headerData(column, Qt.Horizontal, Qt.DisplayRole)


def columnCount(table):
    return table.model().columnCount()


def rowCount(table):
    return table.model().rowCount()


def widgetAt(table, row, column):
    return table.indexWidget(table.model().index(row, column))


def visualRow(table, row):
    return table.verticalHeader().visualIndex(row)