# -*- coding: utf-8 -*-

from PyQt4.QtGui import QLabel, QLineEdit

from test.cute.matchers import named, withBuddy
from test.cute.widgets import (WidgetDriver, LabelDriver, LineEditDriver)

import tgit.tags as tags
from tgit.ui import constants as ui


class TrackPageDriver(WidgetDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(TrackPageDriver, self).__init__(selector, prober, gesturePerformer)

    def showsMetadata(self, **meta):
        for tag, value in meta.iteritems():
            if tag == tags.TRACK_TITLE:
                self.showsTrackTitle(value)
            elif tag == tags.VERSION_INFO:
                self.showsVersionInfo(value)
            elif tag == tags.FEATURED_GUEST:
                self.showsFeaturedGuest(value)
            elif tag == tags.ISRC:
                self.showsIsrc(value)
            elif tag == tags.BITRATE:
                self.showsBitrate(value)
            elif tag == tags.DURATION:
                self.showsDuration(value)
            else:
                raise AssertionError("Don't know how to verify <%s>" % tag)

    def changeMetadata(self, **meta):
        for tag, value in meta.iteritems():
            if tag == tags.TRACK_TITLE:
                self.changeTrackTitle(value)
            elif tag == tags.VERSION_INFO:
                self.changeVersionInfo(value)
            elif tag == tags.FEATURED_GUEST:
                self.changeFeaturedGuest(value)
            elif tag == tags.ISRC:
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