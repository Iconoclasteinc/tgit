# -*- coding: utf-8 -*-

from PyQt4.QtGui import QLabel, QLineEdit

import tgit.ui.track_panel as ui

from test.cute.matchers import named, withBuddy
from test.cute.widgets import (WidgetDriver, LabelDriver, LineEditDriver)

DURATION = 'duration'
BITRATE = 'bitrate'
ISRC = 'isrc'
VERSION_INFO = 'versionInfo'
FEATURED_GUEST = 'featuredGuest'
TRACK_TITLE = 'trackTitle'


class TrackPanelDriver(WidgetDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(TrackPanelDriver, self).__init__(selector, prober, gesturePerformer)

    def showsMetadata(self, **tags):
        for tag, value in tags.iteritems():
            if tag == TRACK_TITLE:
                self.showsTrackTitle(value)
            elif tag == VERSION_INFO:
                self.showsVersionInfo(value)
            elif tag == FEATURED_GUEST:
                self.showsFeaturedGuest(value)
            elif tag == ISRC:
                self.showsIsrc(value)
            elif tag == BITRATE:
                self.showsBitrate(tags[BITRATE])
            elif tag == DURATION:
                self.showsDuration(tags[DURATION])
            else:
                AssertionError("Don't know how to verify <%s>" % tag)

    def changeMetadata(self, **tags):
        for tag, value in tags.iteritems():
            if tag == TRACK_TITLE:
                self.changeTrackTitle(value)
            elif tag == VERSION_INFO:
                self.changeVersionInfo(value)
            elif tag == FEATURED_GUEST:
                self.changeFeaturedGuest(value)
            elif tag == ISRC:
                self.changeIsrc(value)
            else:
                AssertionError("Don't know how to edit <%s>" % tag)

    def showsTrackTitle(self, trackTitle):
        label = LabelDriver.findIn(self, QLabel, withBuddy(named(ui.TRACK_TITLE_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.TRACK_TITLE_NAME))
        edit.hasText(trackTitle)

    def changeTrackTitle(self, title):
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.TRACK_TITLE_NAME))
        edit.replaceAllText(title)

    def showsVersionInfo(self, versionInfo):
        label = LabelDriver.findIn(self, QLabel, withBuddy(named(ui.VERSION_INFO_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.VERSION_INFO_NAME))
        edit.hasText(versionInfo)

    def changeVersionInfo(self, info):
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.VERSION_INFO_NAME))
        edit.replaceAllText(info)

    def showsFeaturedGuest(self, featuredGuest):
        label = LabelDriver.findIn(self, QLabel, withBuddy(named(ui.VERSION_INFO_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.FEATURED_GUEST_NAME))
        edit.hasText(featuredGuest)

    def changeFeaturedGuest(self, name):
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.FEATURED_GUEST_NAME))
        edit.replaceAllText(name)

    def showsIsrc(self, isrc):
        label = LabelDriver.findIn(self, QLabel, withBuddy(named(ui.ISRC_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.ISRC_NAME))
        edit.hasText(isrc)

    def changeIsrc(self, code):
        edit = LineEditDriver.findIn(self, QLineEdit, named(ui.ISRC_NAME))
        edit.replaceAllText(code)

    def showsBitrate(self, text):
        label = LabelDriver.findIn(self, QLabel, withBuddy(named(ui.BITRATE_NAME)))
        label.isShowingOnScreen()
        info = LabelDriver.findIn(self, QLabel, named(ui.BITRATE_NAME))
        info.hasText(text)

    def showsDuration(self, text):
        label = LabelDriver.findIn(self, QLabel, withBuddy(named(ui.DURATION_NAME)))
        label.isShowingOnScreen()
        info = LabelDriver.findIn(self, QLabel, named(ui.DURATION_NAME))
        info.hasText(text)