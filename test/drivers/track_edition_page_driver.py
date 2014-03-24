# -*- coding: utf-8 -*-

from PyQt4.QtGui import QLabel, QLineEdit, QPlainTextEdit, QTimeEdit, QWidget, QComboBox

from test.cute.matchers import named, withBuddy, showingOnScreen, withPixmapHeight, withPixmapWidth
from test.cute.widgets import (WidgetDriver, LabelDriver, LineEditDriver, TextEditDriver,
                               DateTimeEditDriver, ComboBoxDriver)

import tgit.tags as tags
from tgit.ui.views.track_edition_page import TrackEditionPage


def trackEditionPage(parent):
    return TrackEditionPageDriver.findSingle(parent, QWidget, named(TrackEditionPage.NAME), showingOnScreen())


class TrackEditionPageDriver(WidgetDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(TrackEditionPageDriver, self).__init__(selector, prober, gesturePerformer)

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

    def showsAlbumTitle(self, title):
        label = self._label(named(TrackEditionPage.ALBUM_TITLE_BANNER_NAME))
        label.isShowingOnScreen()
        label.hasText(title)

    def showsAlbumLeadPerformer(self, name):
        label = self._label(named(TrackEditionPage.ALBUM_LEAD_PERFORMER_BANNER_NAME))
        label.isShowingOnScreen()
        label.hasText(name)

    def displaysAlbumCover(self):
        label = self._label(named(TrackEditionPage.ALBUM_COVER_BANNER_NAME))
        label.isShowingOnScreen()
        height, width = TrackEditionPage.ALBUM_COVER_BANNER_SIZE
        label.hasPixmap(withPixmapHeight(height))
        label.hasPixmap(withPixmapWidth(width))

    def showsTrackTitle(self, trackTitle):
        label = self._label(withBuddy(named(TrackEditionPage.TRACK_TITLE_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(TrackEditionPage.TRACK_TITLE_FIELD_NAME))
        edit.hasText(trackTitle)

    def changeTrackTitle(self, title):
        edit = self._lineEdit(named(TrackEditionPage.TRACK_TITLE_FIELD_NAME))
        edit.changeText(title)

    def showsLeadPerformer(self, name, disabled=False):
        label = self._label(withBuddy(named(TrackEditionPage.LEAD_PERFORMER_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(TrackEditionPage.LEAD_PERFORMER_FIELD_NAME))
        edit.hasText(name)
        edit.isDisabled(disabled)

    def changeLeadPerformer(self, name):
        edit = self._lineEdit(named(TrackEditionPage.LEAD_PERFORMER_FIELD_NAME))
        edit.changeText(name)

    def showsVersionInfo(self, versionInfo):
        label = self._label(withBuddy(named(TrackEditionPage.VERSION_INFO_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(TrackEditionPage.VERSION_INFO_FIELD_NAME))
        edit.hasText(versionInfo)

    def changeVersionInfo(self, info):
        edit = LineEditDriver.findSingle(self, QLineEdit, named(TrackEditionPage.VERSION_INFO_FIELD_NAME))
        edit.changeText(info)

    def showsBitrate(self, text):
        label = self._label(withBuddy(named(TrackEditionPage.BITRATE_FIELD_NAME)))
        label.isShowingOnScreen()
        value = self._label(named(TrackEditionPage.BITRATE_FIELD_NAME))
        value.hasText(text)

    def showsTrackNumber(self, number):
        label = self._label(named(TrackEditionPage.TRACK_NUMBER_BANNER_NAME))
        label.isShowingOnScreen()
        label.hasText(number)

    def showsDuration(self, text):
        label = self._label(withBuddy(named(TrackEditionPage.DURATION_FIELD_NAME)))
        label.isShowingOnScreen()
        value = self._label(named(TrackEditionPage.DURATION_FIELD_NAME))
        value.hasText(text)

    def showsFeaturedGuest(self, name):
        label = self._label(withBuddy(named(TrackEditionPage.FEATURED_GUEST_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(TrackEditionPage.FEATURED_GUEST_FIELD_NAME))
        edit.hasText(name)

    def changeFeaturedGuest(self, name):
        edit = self._lineEdit(named(TrackEditionPage.FEATURED_GUEST_FIELD_NAME))
        edit.changeText(name)

    def showsLyricist(self, name):
        label = self._label(withBuddy(named(TrackEditionPage.LYRICIST_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(TrackEditionPage.LYRICIST_FIELD_NAME))
        edit.hasText(name)

    def changeLyricist(self, name):
        edit = self._lineEdit(named(TrackEditionPage.LYRICIST_FIELD_NAME))
        edit.changeText(name)

    def showsComposer(self, name):
        label = self._label(withBuddy(named(TrackEditionPage.COMPOSER_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(TrackEditionPage.COMPOSER_FIELD_NAME))
        edit.hasText(name)

    def changeComposer(self, name):
        edit = self._lineEdit(named(TrackEditionPage.COMPOSER_FIELD_NAME))
        edit.changeText(name)

    def showsPublisher(self, name):
        label = self._label(withBuddy(named(TrackEditionPage.PUBLISHER_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(TrackEditionPage.PUBLISHER_FIELD_NAME))
        edit.hasText(name)

    def changePublisher(self, name):
        edit = self._lineEdit(named(TrackEditionPage.PUBLISHER_FIELD_NAME))
        edit.changeText(name)

    def showsIsrc(self, code):
        label = self._label(withBuddy(named(TrackEditionPage.ISRC_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(TrackEditionPage.ISRC_FIELD_NAME))
        edit.hasText(code)

    def changeIsrc(self, code):
        edit = self._lineEdit(named(TrackEditionPage.ISRC_FIELD_NAME))
        edit.changeText(code)

    def showsIswc(self, code):
        label = self._label(withBuddy(named(TrackEditionPage.ISWC_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(TrackEditionPage.ISWC_FIELD_NAME))
        edit.isDisabled()
        edit.hasText(code)

    def showsTags(self, tags):
        label = self._label(withBuddy(named(TrackEditionPage.TAGS_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._lineEdit(named(TrackEditionPage.TAGS_FIELD_NAME))
        edit.hasText(tags)

    def changeTags(self, tags):
        edit = self._lineEdit(named(TrackEditionPage.TAGS_FIELD_NAME))
        edit.changeText(tags)

    def _textEdit(self, matching):
        return TextEditDriver.findSingle(self, QPlainTextEdit, matching)

    def showsLyrics(self, lyrics):
        label = self._label(withBuddy(named(TrackEditionPage.LYRICS_FIELD_NAME)))
        label.isShowingOnScreen()
        edit = self._textEdit(named(TrackEditionPage.LYRICS_FIELD_NAME))
        edit.hasPlainText(lyrics)

    def addLyrics(self, *lyrics):
        edit = self._textEdit(named(TrackEditionPage.LYRICS_FIELD_NAME))
        for lyric in lyrics:
            edit.addLine(lyric)
        edit.clearFocus()

    def showsLanguage(self, lang):
        label = self._label(withBuddy(named(TrackEditionPage.LANGUAGE_FIELD_NAME)))
        label.isShowingOnScreen()
        combo = self._combobox(named(TrackEditionPage.LANGUAGE_FIELD_NAME))
        combo.hasCurrentText(lang)

    def changeLanguage(self, lang):
        combo = self._combobox(named(TrackEditionPage.LANGUAGE_FIELD_NAME))
        combo.changeText(lang)

    def selectLanguage(self, lang):
        combo = self._combobox(named(TrackEditionPage.LANGUAGE_FIELD_NAME))
        combo.selectOption(lang)

    def showsPreviewTime(self, time):
        edit = self._dateTimeEdit(named(TrackEditionPage.PREVIEW_TIME_FIELD_NAME))
        edit.hasTime(time)

    def _dateTimeEdit(self, matching):
        return DateTimeEditDriver.findSingle(self, QTimeEdit, matching)

    def _combobox(self, matching):
        return ComboBoxDriver.findSingle(self, QComboBox, matching)