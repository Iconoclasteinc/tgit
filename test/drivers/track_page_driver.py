# -*- coding: utf-8 -*-

from PyQt4.QtGui import QLabel, QLineEdit

from test.cute.matchers import named, withBuddy
from test.cute.widgets import (WidgetDriver, LabelDriver, LineEditDriver)

import tgit.track as track
from tgit.ui import constants as ui


class TrackPageDriver(WidgetDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(TrackPageDriver, self).__init__(selector, prober, gesturePerformer)

    def showsMetadata(self, **tags):
        for tag, value in tags.iteritems():
            if tag == track.TITLE:
                self.showsTrackTitle(value)
            elif tag == track.VERSION_INFO:
                self.showsVersionInfo(value)
            elif tag == track.FEATURED_GUEST:
                self.showsFeaturedGuest(value)
            elif tag == track.ISRC:
                self.showsIsrc(value)
            elif tag == track.BITRATE:
                self.showsBitrate(value)
            elif tag == track.DURATION:
                self.showsDuration(value)
            else:
                raise AssertionError("Don't know how to verify <%s>" % tag)

    def changeMetadata(self, **tags):
        for tag, value in tags.iteritems():
            if tag == track.TITLE:
                self.changeTrackTitle(value)
            elif tag == track.VERSION_INFO:
                self.changeVersionInfo(value)
            elif tag == track.FEATURED_GUEST:
                self.changeFeaturedGuest(value)
            elif tag == track.ISRC:
                self.changeIsrc(value)
            else:
                raise AssertionError("Don't know how to edit <%s>" % tag)

    def showsTrackTitle(self, trackTitle):
        label = LabelDriver.findSingle(self, QLabel, withBuddy(named(ui.TRACK_TITLE_EDIT_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.TRACK_TITLE_EDIT_NAME))
        edit.hasText(trackTitle)

    def changeTrackTitle(self, title):
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.TRACK_TITLE_EDIT_NAME))
        edit.replaceAllText(title)

    def showsVersionInfo(self, versionInfo):
        label = LabelDriver.findSingle(self, QLabel, withBuddy(named(ui.VERSION_INFO_EDIT_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.VERSION_INFO_EDIT_NAME))
        edit.hasText(versionInfo)

    def changeVersionInfo(self, info):
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.VERSION_INFO_EDIT_NAME))
        edit.replaceAllText(info)

    def showsFeaturedGuest(self, featuredGuest):
        label = LabelDriver.findSingle(self, QLabel, withBuddy(named(ui.VERSION_INFO_EDIT_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.FEATURED_GUEST_EDIT_NAME))
        edit.hasText(featuredGuest)

    def changeFeaturedGuest(self, name):
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.FEATURED_GUEST_EDIT_NAME))
        edit.replaceAllText(name)

    def showsIsrc(self, isrc):
        label = LabelDriver.findSingle(self, QLabel, withBuddy(named(ui.ISRC_EDIT_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.ISRC_EDIT_NAME))
        edit.hasText(isrc)

    def changeIsrc(self, code):
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.ISRC_EDIT_NAME))
        edit.replaceAllText(code)

    def showsBitrate(self, text):
        label = LabelDriver.findSingle(self, QLabel, withBuddy(named(ui.BITRATE_NAME)))
        label.isShowingOnScreen()
        info = LabelDriver.findSingle(self, QLabel, named(ui.BITRATE_NAME))
        info.hasText(text)

    def showsDuration(self, text):
        label = LabelDriver.findSingle(self, QLabel, withBuddy(named(ui.DURATION_NAME)))
        label.isShowingOnScreen()
        info = LabelDriver.findSingle(self, QLabel, named(ui.DURATION_NAME))
        info.hasText(text)