from PyQt4.QtGui import QLabel, QLineEdit

from tests.cute.matchers import named, withBuddy
from tests.cute.widgets import (WidgetDriver, LabelDriver, LineEditDriver)

import tgit.ui.track_panel as ui


class TrackPanelDriver(WidgetDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(TrackPanelDriver, self).__init__(selector, prober, gesturePerformer)

    def showsTrackTitle(self, trackTitle):
        label = LabelDriver.find(self, QLabel, withBuddy(named(ui.TRACK_TITLE_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.find(self, QLineEdit, named(ui.TRACK_TITLE_NAME))
        edit.hasText(trackTitle)

    def changeTrackTitle(self, title):
        edit = LineEditDriver.find(self, QLineEdit, named(ui.TRACK_TITLE_NAME))
        edit.replaceAllText(title)

    def showsVersionInfo(self, versionInfo):
        label = LabelDriver.find(self, QLabel, withBuddy(named(ui.VERSION_INFO_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.find(self, QLineEdit, named(ui.VERSION_INFO_NAME))
        edit.hasText(versionInfo)

    def changeVersionInfo(self, info):
        edit = LineEditDriver.find(self, QLineEdit, named(ui.VERSION_INFO_NAME))
        edit.replaceAllText(info)

    def showsFeaturedGuest(self, featuredGuest):
        label = LabelDriver.find(self, QLabel, withBuddy(named(ui.VERSION_INFO_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.find(self, QLineEdit, named(ui.FEATURED_GUEST_NAME))
        edit.hasText(featuredGuest)

    def changeFeaturedGuest(self, name):
        edit = LineEditDriver.find(self, QLineEdit, named(ui.FEATURED_GUEST_NAME))
        edit.replaceAllText(name)

    def showsIsrc(self, isrc):
        label = LabelDriver.find(self, QLabel, withBuddy(named(ui.ISRC_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.find(self, QLineEdit, named(ui.ISRC_NAME))
        edit.hasText(isrc)

    def changeIsrc(self, code):
        edit = LineEditDriver.find(self, QLineEdit, named(ui.ISRC_NAME))
        edit.replaceAllText(code)

    def showsBitrate(self, text):
        label = LabelDriver.find(self, QLabel, withBuddy(named(ui.BITRATE_NAME)))
        label.isShowingOnScreen()
        info = LabelDriver.find(self, QLabel, named(ui.BITRATE_NAME))
        info.hasText(text)

    def showsDuration(self, text):
        label = LabelDriver.find(self, QLabel, withBuddy(named(ui.DURATION_NAME)))
        label.isShowingOnScreen()
        info = LabelDriver.find(self, QLabel, named(ui.DURATION_NAME))
        info.hasText(text)