# -*- coding: utf-8 -*-

from PyQt4.QtGui import QLabel, QLineEdit, QPlainTextEdit, QTimeEdit, QWidget

from test.cute.matchers import named, withBuddy, showingOnScreen
from test.cute.widgets import (WidgetDriver, LabelDriver, LineEditDriver, TextEditDriver,
                               DateTimeEditDriver)

import tgit.tags as tags
from tgit.ui.views.track_page import TrackPage


def trackPage(parent):
    return TrackPageDriver.findSingle(parent, QWidget, named(TrackPage.NAME), showingOnScreen())


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
            elif tag == 'trackNumber':
                self.showsTrackNumber(value)
            elif tag == 'totalTracks':
                self.showsTotalTracks(value)
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

    def _label(self, matching):
        return LabelDriver.findSingle(self, QLabel, matching)

    def _lineEdit(self, matching):
        return LineEditDriver.findSingle(self, QLineEdit, matching)

    def showsTrackTitle(self, trackTitle):
        label = self._label(withBuddy(named(TrackPage.TRACK_TITLE_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(TrackPage.TRACK_TITLE_FIELD_NAME))
        edit.hasText(trackTitle)

    def changeTrackTitle(self, title):
        edit = self._lineEdit(named(TrackPage.TRACK_TITLE_FIELD_NAME))
        edit.changeText(title)

    def showsVersionInfo(self, versionInfo):
        label = self._label(withBuddy(named(TrackPage.VERSION_INFO_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(TrackPage.VERSION_INFO_FIELD_NAME))
        edit.hasText(versionInfo)

    def changeVersionInfo(self, info):
        edit = LineEditDriver.findSingle(self, QLineEdit, named(TrackPage.VERSION_INFO_FIELD_NAME))
        edit.changeText(info)

    def showsBitrate(self, text):
        label = self._label(withBuddy(named(TrackPage.BITRATE_FIELD_NAME)))
        label.isShowingOnScreen()
        value = self._label(named(TrackPage.BITRATE_FIELD_NAME))
        value.hasText(text)

    def showsTrackNumber(self, number):
        label = self._label(withBuddy(named(TrackPage.TRACK_NUMBER_FIELD_NAME)))
        label.isShowingOnScreen()
        value = self._label(named(TrackPage.TRACK_NUMBER_FIELD_NAME))
        value.hasText(number)

    def showsTotalTracks(self, count):
        label = self._label(withBuddy(named(TrackPage.TOTAL_TRACKS_FIELD_NAME)))
        label.isShowingOnScreen()
        value = self._label(named(TrackPage.TOTAL_TRACKS_FIELD_NAME))
        value.hasText(count)

    def showsDuration(self, text):
        label = self._label(withBuddy(named(TrackPage.DURATION_FIELD_NAME)))
        label.isShowingOnScreen()
        value = self._label(named(TrackPage.DURATION_FIELD_NAME))
        value.hasText(text)

    def showsFeaturedGuest(self, name):
        label = self._label(withBuddy(named(TrackPage.FEATURED_GUEST_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(TrackPage.FEATURED_GUEST_FIELD_NAME))
        edit.hasText(name)

    def changeFeaturedGuest(self, name):
        edit = self._lineEdit(named(TrackPage.FEATURED_GUEST_FIELD_NAME))
        edit.changeText(name)

    def showsLyricist(self, name):
        label = self._label(withBuddy(named(TrackPage.LYRICIST_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(TrackPage.LYRICIST_FIELD_NAME))
        edit.hasText(name)

    def changeLyricist(self, name):
        edit = self._lineEdit(named(TrackPage.LYRICIST_FIELD_NAME))
        edit.changeText(name)

    def showsComposer(self, name):
        label = self._label(withBuddy(named(TrackPage.COMPOSER_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(TrackPage.COMPOSER_FIELD_NAME))
        edit.hasText(name)

    def changeComposer(self, name):
        edit = self._lineEdit(named(TrackPage.COMPOSER_FIELD_NAME))
        edit.changeText(name)

    def showsPublisher(self, name):
        label = self._label(withBuddy(named(TrackPage.PUBLISHER_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(TrackPage.PUBLISHER_FIELD_NAME))
        edit.hasText(name)

    def changePublisher(self, name):
        edit = self._lineEdit(named(TrackPage.PUBLISHER_FIELD_NAME))
        edit.changeText(name)

    def showsIsrc(self, code):
        label = self._label(withBuddy(named(TrackPage.ISRC_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(TrackPage.ISRC_FIELD_NAME))
        edit.hasText(code)

    def changeIsrc(self, code):
        edit = self._lineEdit(named(TrackPage.ISRC_FIELD_NAME))
        edit.changeText(code)

    def showsIswc(self, code):
        label = self._label(withBuddy(named(TrackPage.ISWC_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(TrackPage.ISWC_FIELD_NAME))
        edit.isDisabled()
        edit.hasText(code)

    def showsTags(self, tags):
        label = self._label(withBuddy(named(TrackPage.TAGS_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(TrackPage.TAGS_FIELD_NAME))
        edit.hasText(tags)

    def changeTags(self, tags):
        edit = self._lineEdit(named(TrackPage.TAGS_FIELD_NAME))
        edit.changeText(tags)

    def _textEdit(self, matching):
        return TextEditDriver.findSingle(self, QPlainTextEdit, matching)

    def showsLyrics(self, lyrics):
        label = self._label(withBuddy(named(TrackPage.LYRICS_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._textEdit(named(TrackPage.LYRICS_FIELD_NAME))
        edit.hasPlainText(lyrics)

    def addLyrics(self, *lyrics):
        edit = self._textEdit(named(TrackPage.LYRICS_FIELD_NAME))
        for lyric in lyrics:
            edit.addLine(lyric)
        edit.clearFocus()

    def showsLanguage(self, text):
        label = self._label(withBuddy(named(TrackPage.LANGUAGE_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(TrackPage.LANGUAGE_FIELD_NAME))
        edit.hasText(text)

    def changeLanguage(self, tags):
        edit = self._lineEdit(named(TrackPage.LANGUAGE_FIELD_NAME))
        edit.changeText(tags)

    def _dateTimeEdit(self, matching):
        return DateTimeEditDriver.findSingle(self, QTimeEdit, matching)

    def showsPreviewTime(self, time):
        edit = self._dateTimeEdit(named(TrackPage.PREVIEW_TIME_FIELD_NAME))
        edit.hasTime(time)