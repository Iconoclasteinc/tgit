# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from hamcrest.library.text import contains_string

from test.cute.matchers import named
from test.drivers.__base import BaseDriver
from test.drivers.album_edition_page_driver import albumEditionPage
from test.drivers.album_composition_page_driver import albumCompositionPage
from test.drivers.track_edition_page_driver import trackEditionPage


def albumScreen(parent):
    return AlbumScreenDriver.findSingle(parent, QWidget, named('album-screen'))


def isDisabled(button):
    button.isDisabled()
    button.hasCursorShape(Qt.ArrowCursor)


def isEnabled(button):
    button.isEnabled()
    button.hasCursorShape(Qt.PointingHandCursor)


class AlbumScreenDriver(BaseDriver):
    def isShowingAlbumCompositionPage(self):
        albumCompositionPage(self).isShowingOnScreen()
        isDisabled(self.button(named('previous')))
        isDisabled(self.button(named('save')))

    def isShowingAlbumEditionPage(self):
        albumEditionPage(self).isShowingOnScreen()
        isEnabled(self.button(named('previous')))
        isEnabled(self.button(named('save')))

    def isShowingTrackEditionPage(self):
        trackEditionPage(self).isShowingOnScreen()
        isEnabled(self.button(named('previous')))
        isEnabled(self.button(named('save')))

    def addFiles(self):
        albumCompositionPage(self).addFiles()

    def removeTrack(self, title):
        albumCompositionPage(self).removeTrack(title)

    def moveTrack(self, title, to):
        albumCompositionPage(self).moveTrack(title, to)

    def previousPage(self):
        button = self.button(named('previous'))
        button.isEnabled()
        button.click()

    def nextPage(self):
        button = self.button(named('next'))
        isEnabled(button)
        button.click()

    def save(self):
        self.button(named('save')).click()

    def hasDisabledNextPageButton(self):
        isDisabled(self.button(named('next')))

    def hasEnabledNextPageButton(self):
        isEnabled(self.button(named('next')))

    def hasDisabledPreviousPageButton(self):
        isDisabled(self.button(named('previous')))

    def hasEnabledPreviousPageButton(self):
        isEnabled(self.button(named('previous')))

    def hasDisabledSaveButton(self):
        isDisabled(self.button(named('save')))

    def hasEnabledSaveButton(self):
        isEnabled(self.button(named('save')))

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
        self.label(named('help-link')).hasText(contains_string('href="%s"' % location))

    def linksFeatureRequestTo(self, location):
        self.label(named('feature-request-link')).hasText(contains_string('href="%s' % location))

    def showsPage(self, matching):
        return self.widget(matching).isShowingOnScreen()