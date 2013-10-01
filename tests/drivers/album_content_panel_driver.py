# -*- coding: utf-8 -*-

from PyQt4.QtGui import QLabel, QPushButton
from hamcrest.library import contains_string

from tgit.ui import album_content_panel as ui

from tests.cute.widgets import WidgetDriver, LabelDriver, AbstractButtonDriver
from tests.cute.matchers import named, withLabelText, withButtonText


class AlbumContentPanelDriver(WidgetDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(AlbumContentPanelDriver, self).__init__(selector, prober, gesturePerformer)

    def _showsLabel(self, title):
        LabelDriver.find(self, QLabel, withLabelText(title)).isShowingOnScreen()

    def showsTrackTitle(self, title):
        self._showsLabel(title)

    def showsTrackDuration(self, duration):
        self._showsLabel(duration)

    def showsTitleHeader(self, title):
        label = LabelDriver.find(self, QLabel, named(ui.TRACK_TITLE_HEADER_NAME))
        label.hasText(contains_string(title))

    def showsDurationHeader(self, duration):
        label = LabelDriver.find(self, QLabel, named(ui.TRACK_DURATION_HEADER_NAME))
        label.hasText(contains_string(duration))

    def showsColumnHeadings(self, title, duration):
        self.showsTitleHeader(title)
        self.showsDurationHeader(duration)

    def playTrack(self):
        button = self._locatePlayButton()
        button.isUp()
        button.click()
        button.isDown()

    def _locatePlayButton(self):
        button = AbstractButtonDriver.find(self, QPushButton, withButtonText('Play'))
        button.isShowingOnScreen()
        return button

    def pauseTrack(self):
        button = self._locatePlayButton()
        button.isDown()
        button.click()
        button.isUp()