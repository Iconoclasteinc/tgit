# -*- coding: utf-8 -*-

from PyQt4.Qt import (QApplication, QMainWindow, QLineEdit, QPushButton, QListView,
                      QToolButton, QDir, QFileDialog)
from hamcrest.core import all_of, equal_to

from tests.cute.probes import (WidgetManipulatorProbe, WidgetAssertionProbe,
                               WidgetPropertyAssertionProbe, WidgetScreenBoundsProbe)
from tests.cute.finders import SingleWidgetFinder, TopLevelWidgetsFinder, RecursiveWidgetFinder
from tests.cute import properties, gestures, keyboard_shortcuts as shortcuts, matchers as match


def mainWindow(*matchers):
    return SingleWidgetFinder(RecursiveWidgetFinder(QMainWindow, all_of(*matchers),
                                                    TopLevelWidgetsFinder(QApplication.instance())))


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
    def find(cls, parent, widgetType, *matchers):
        return cls(SingleWidgetFinder(
                   RecursiveWidgetFinder(widgetType, all_of(*matchers), parent.selector)),
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
    def click(self):
        return self.leftClickOnWidget()


class LabelDriver(WidgetDriver):
    def hasText(self, text):
        self.has(properties.labelText(), equal_to(text))

    def hasPixmap(self, matcher):
        self.has(properties.labelPixmap(), matcher)


class LineEditDriver(WidgetDriver):
    EDITION_DELAY = 50

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
    NAVIGATION_DELAY = 100

    def showHiddenFiles(self):
        class ShowHiddenFiles(object):
            def __call__(self, dialog):
                dialog.setFilter(dialog.filter() | QDir.Hidden)

        self.manipulate("show hidden files", ShowHiddenFiles())

    def navigateToDir(self, path):
        for folderName in self._navigationPathTo(path):
            if folderName == '..':
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
        return AbstractButtonDriver.find(self, QToolButton, match.named(name))

    def enterManually(self, filename):
        self._filenameEdit().replaceAllText(filename)

    def accept(self):
        self._acceptButton().click()

    def _listView(self):
        return ListViewDriver.find(self, QListView, match.named('listView'))

    def _filenameEdit(self):
        return LineEditDriver.find(self, QLineEdit, match.named("fileNameEdit"))

    def _acceptButton(self):
        class FindOutAcceptButtonText(object):
            def __call__(self, dialog):
                self.text = dialog.labelText(QFileDialog.Accept)

        acceptButton = FindOutAcceptButtonText()
        self.manipulate("find out accept button text", acceptButton)
        return AbstractButtonDriver.find(self, QPushButton, match.withButtonText(acceptButton.text))


class ListViewDriver(WidgetDriver):
    def selectItem(self, matcher):
        self._selectItem(self._indexOfFirstItemMatching(matcher))

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

    def _indexOfFirstItemMatching(self, matcher):
        from hamcrest.core.base_matcher import BaseMatcher

        class ItemMatcher(BaseMatcher):
            def __init__(self, matcher):
                super(ItemMatcher, self).__init__()
                self._itemMatcher = matcher

            def _matches(self, listView):
                model = listView.model()
                root = listView.rootIndex()
                itemCount = model.rowCount(root)
                for i in range(itemCount):
                    index = model.index(i, 0, root)
                    if self._itemMatcher.matches(index):
                        self.index = index
                        return True

                return False

            def describe_to(self, description):
                description.append_text("containing an item ")
                self._itemMatcher.describe_to(description)

            def describe_mismatch(self, item, mismatch_description):
                mismatch_description.append_text("was not containing ")
                self._itemMatcher.describe_to(mismatch_description)

        itemFound = ItemMatcher(matcher)
        self.is_(itemFound)
        return itemFound.index




