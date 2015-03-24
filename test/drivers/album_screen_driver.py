# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from hamcrest.library.text import contains_string

from test.cute.matchers import named
from test.drivers import BaseDriver
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
    def showsAlbumCompositionPage(self):
        albumCompositionPage(self).isShowingOnScreen()

    def showsAlbumEditionPage(self):
        albumEditionPage(self).isShowingOnScreen()

    def showsTrackEditionPage(self):
        trackEditionPage(self).isShowingOnScreen()

    def addFiles(self):
        albumCompositionPage(self).addFiles()

    def removeTrack(self, title):
        albumCompositionPage(self).removeTrack(title)

    def moveTrack(self, title, to):
        albumCompositionPage(self).moveTrack(title, to)

    def previousPage(self):
        self.button(named('previous')).click()

    def nextPage(self):
        self.button(named('next')).click()

    def save(self):
        self.button(named('save')).click()

    def hidesPreviousPageButton(self):
        isDisabled(self.button(named('previous')))

    def showsPreviousPageButton(self):
        isEnabled(self.button(named('previous')))

    def hidesNextPageButton(self):
        isDisabled(self.button(named('next')))

    def showsNextPageButton(self):
        isEnabled(self.button(named('next')))

    def hidesSaveButton(self):
        isDisabled(self.button(named('save')))

    def showsSaveButton(self):
        isEnabled(self.button(named('save')))

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