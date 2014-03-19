# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from hamcrest.library.text import contains_string

from test.cute.widgets import WidgetDriver, ButtonDriver, LabelDriver
from test.cute.matchers import named
from test.drivers.album_edition_page_driver import albumEditionPage
from test.drivers.album_composition_page_driver import albumCompositionPage
from test.drivers.track_edition_page_driver import trackEditionPage

from tgit.ui.views.album_screen import AlbumScreen


def albumScreen(parent):
    return AlbumScreenDriver.findSingle(parent, QWidget, named(AlbumScreen.NAME))


def isDisabled(button):
    button.isDisabled()
    button.hasCursorShape(Qt.ArrowCursor)


def isEnabled(button):
    button.isEnabled()
    button.hasCursorShape(Qt.PointingHandCursor)


class Buttons(object):
    PREVIOUS = named(AlbumScreen.PREVIOUS_PAGE_BUTTON_NAME)
    NEXT = named(AlbumScreen.NEXT_PAGE_BUTTON_NAME)
    SAVE = named(AlbumScreen.SAVE_BUTTON_NAME)


class AlbumScreenDriver(WidgetDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(AlbumScreenDriver, self).__init__(selector, prober, gesturePerformer)

    def isShowingAlbumCompositionPage(self):
        albumCompositionPage(self).isShowingOnScreen()
        isDisabled(self._button(Buttons.PREVIOUS))
        isDisabled(self._button(Buttons.SAVE))

    def isShowingAlbumEditionPage(self):
        albumEditionPage(self).isShowingOnScreen()
        isEnabled(self._button(Buttons.PREVIOUS))
        isEnabled(self._button(Buttons.SAVE))

    def isShowingTrackEditionPage(self):
        trackEditionPage(self).isShowingOnScreen()
        isEnabled(self._button(Buttons.PREVIOUS))
        isEnabled(self._button(Buttons.SAVE))

    def addFiles(self):
        albumCompositionPage(self).addFiles()

    def removeTrack(self, title):
        albumCompositionPage(self).removeTrack(title)

    def moveTrack(self, title, to):
        albumCompositionPage(self).moveTrack(title, to)

    def previousPage(self):
        button = self._button(Buttons.PREVIOUS)
        button.isEnabled()
        button.click()

    def nextPage(self):
        button = self._button(Buttons.NEXT)
        isEnabled(button)
        button.click()

    def save(self):
        self._button(Buttons.SAVE).click()

    def hasDisabledNextPageButton(self):
        isDisabled(self._button(Buttons.NEXT))

    def hasEnabledNextPageButton(self):
        isEnabled(self._button(Buttons.NEXT))

    def hasDisabledPreviousPageButton(self):
        isDisabled(self._button(Buttons.PREVIOUS))

    def hasEnabledPreviousPageButton(self):
        isEnabled(self._button(Buttons.PREVIOUS))

    def hasDisabledSaveButton(self):
        isDisabled(self._button(Buttons.SAVE))

    def hasEnabledSaveButton(self):
        isEnabled(self._button(Buttons.SAVE))

    def navigateToAlbumMetadata(self):
        self.nextPage()
        self.isShowingAlbumEditionPage()

    # todo have a quick navigation button
    def navigateToTrackMetadata(self):
        self.nextPage()
        self.isShowingTrackEditionPage()

    def showsAlbumContains(self, *tracks):
        albumCompositionPage(self).showsTracksInOrder(*tracks)

    def showsAlbumMetadata(self, **tags):
        albumEditionPage(self).showsMetadata(**tags)

    def editAlbumMetadata(self, **tags):
        albumEditionPage(self).changeMetadata(**tags)

    def showsTrackMetadata(self, **tags):
        trackEditionPage(self).showsMetadata(**tags)

    def editTrackMetadata(self, **tags):
        trackEditionPage(self).changeMetadata(**tags)

    def linksHelpTo(self, location):
        help = LabelDriver.findSingle(self, QLabel, named(AlbumScreen.HELP_LINK_NAME))
        help.hasText(contains_string('href="%s"' % location))

    def linksFeatureRequestTo(self, location):
        help = LabelDriver.findSingle(self, QLabel, named(AlbumScreen.FEATURE_REQUEST_LINK_NAME))
        help.hasText(contains_string('href="%s' % location))

    def _button(self, matching):
        return ButtonDriver.findSingle(self, QPushButton, matching)

    def _page(self, matching):
        return WidgetDriver.findSingle(self, QWidget, matching)

    def containsPage(self, matching):
        return self._page(matching).exists()

    def showsPage(self, matching):
        return self._page(matching).isShowingOnScreen()