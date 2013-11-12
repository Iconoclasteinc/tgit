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
            elif tag == tags.LYRICIST:
                self.showsLyricist(value)
            elif tag == tags.COMPOSER:
                self.showsComposer(value)
            elif tag == tags.PUBLISHER:
                self.showsPublisher(value)
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
            elif tag == tags.LYRICIST:
                self.changeLyricist(value)
            elif tag == tags.COMPOSER:
                self.changeComposer(value)
            elif tag == tags.PUBLISHER:
                self.changePublisher(value)
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

    def showsFeaturedGuest(self, name):
        label = LabelDriver.findSingle(self, QLabel, withBuddy(named(ui.VERSION_INFO_EDIT_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.FEATURED_GUEST_EDIT_NAME))
        edit.hasText(name)

    def changeFeaturedGuest(self, name):
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.FEATURED_GUEST_EDIT_NAME))
        edit.replaceAllText(name)

    def showsLyricist(self, name):
        label = LabelDriver.findSingle(self, QLabel, withBuddy(named(ui.LYRICIST_EDIT_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.LYRICIST_EDIT_NAME))
        edit.hasText(name)

    def changeLyricist(self, name):
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.LYRICIST_EDIT_NAME))
        edit.replaceAllText(name)

    def showsComposer(self, name):
        label = LabelDriver.findSingle(self, QLabel, withBuddy(named(ui.COMPOSER_EDIT_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.COMPOSER_EDIT_NAME))
        edit.hasText(name)

    def changeComposer(self, name):
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.COMPOSER_EDIT_NAME))
        edit.replaceAllText(name)

    def showsPublisher(self, name):
        label = LabelDriver.findSingle(self, QLabel, withBuddy(named(ui.PUBLISHER_EDIT_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.PUBLISHER_EDIT_NAME))
        edit.hasText(name)

    def changePublisher(self, name):
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.PUBLISHER_EDIT_NAME))
        edit.replaceAllText(name)

    def showsIsrc(self, isrc):
        label = LabelDriver.findSingle(self, QLabel, withBuddy(named(ui.ISRC_EDIT_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.ISRC_EDIT_NAME))
        edit.hasText(isrc)

    def changeIsrc(self, code):
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.ISRC_EDIT_NAME))
        edit.replaceAllText(code)

    def showsTags(self, tags):
        label = LabelDriver.findSingle(self, QLabel, withBuddy(named(ui.TAGS_EDIT_NAME)))
        label.isShowingOnScreen()
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.TAGS_EDIT_NAME))
        edit.hasText(tags)

    def changeTags(self, tags):
        edit = LineEditDriver.findSingle(self, QLineEdit, named(ui.TAGS_EDIT_NAME))
        edit.replaceAllText(tags)

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