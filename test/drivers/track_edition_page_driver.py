# -*- coding: utf-8 -*-

from PyQt4.QtGui import QWidget

from test.cute.matchers import named, withBuddy, showingOnScreen, withPixmapHeight, withPixmapWidth
from test.drivers.__base import BaseDriver
from tgit.ui.track_edition_page import TrackEditionPage


def trackEditionPage(parent):
    return TrackEditionPageDriver.findSingle(parent, QWidget, named('track-edition-page'), showingOnScreen())


class TrackEditionPageDriver(BaseDriver):
    def showsMetadata(self, **meta):
        for tag, value in meta.iteritems():
            if tag == 'trackTitle':
                self.showsTrackTitle(value)
            elif tag == 'versionInfo':
                self.showsVersionInfo(value)
            elif tag == 'featuredGuest':
                self.showsFeaturedGuest(value)
            elif tag == 'lyricist':
                self.showsLyricist(value)
            elif tag == 'composer':
                self.showsComposer(value)
            elif tag == 'publichser':
                self.showsPublisher(value)
            elif tag == 'isrc':
                self.showsIsrc(value)
            elif tag == 'bitrate':
                self.showsBitrate(value)
            elif tag == 'duration':
                self.showsDuration(value)
            elif tag == 'trackNumber':
                self.showsTrackNumber(value)
            else:
                raise AssertionError("Don't know how to verify <%s>" % tag)

    def changeMetadata(self, **meta):
        for tag, value in meta.iteritems():
            if tag == 'trackTitle':
                self.changeTrackTitle(value)
            elif tag == 'versionInfo':
                self.changeVersionInfo(value)
            elif tag == 'featuredGuest':
                self.changeFeaturedGuest(value)
            elif tag == 'lyricist':
                self.changeLyricist(value)
            elif tag == 'composer':
                self.changeComposer(value)
            elif tag == 'publisher':
                self.changePublisher(value)
            elif tag == 'isrc':
                self.changeIsrc(value)
            else:
                raise AssertionError("Don't know how to edit <%s>" % tag)

    def displaysAlbumCover(self):
        label = self.label(named('album-cover'))
        label.isShowingOnScreen()
        height, width = TrackEditionPage.ALBUM_COVER_SIZE
        label.hasPixmap(withPixmapHeight(height))
        label.hasPixmap(withPixmapWidth(width))

    def showsAlbumLeadPerformer(self, name):
        label = self.label(named('album-lead-performer'))
        label.isShowingOnScreen()
        label.hasText(name)

    def showsAlbumTitle(self, title):
        label = self.label(named('album-title'))
        label.isShowingOnScreen()
        label.hasText(title)

    def showsAlbumLabel(self, name):
        label = self.label(named('record-label'))
        label.isShowingOnScreen()
        label.hasText(name)

    def showsTrackNumber(self, number):
        label = self.label(named('track-number'))
        label.isShowingOnScreen()
        label.hasText(number)

    def showsTrackTitle(self, trackTitle):
        self.label(withBuddy(named('track-title'))).isShowingOnScreen()
        self.lineEdit(named('track-title')).hasText(trackTitle)

    def changeTrackTitle(self, title):
        self.lineEdit(named('track-title')).changeText(title)

    def showsLeadPerformer(self, name, disabled=False):
        self.label(withBuddy(named('lead-performer'))).isShowingOnScreen()
        edit = self.lineEdit(named('lead-performer'))
        edit.hasText(name)
        edit.isDisabled(disabled)

    def changeLeadPerformer(self, name):
        self.lineEdit(named('lead-performer')).changeText(name)

    def showsVersionInfo(self, versionInfo):
        self.label(withBuddy(named('version-info'))).isShowingOnScreen()
        self.lineEdit(named('version-info')).hasText(versionInfo)

    def changeVersionInfo(self, info):
        self.lineEdit(named('version-info')).changeText(info)

    def showsFeaturedGuest(self, name):
        self.label(withBuddy(named('featured-guest'))).isShowingOnScreen()
        self.lineEdit(named('featured-guest')).hasText(name)

    def changeFeaturedGuest(self, name):
        self.lineEdit(named('featured-guest')).changeText(name)

    def showsLyricist(self, name):
        self.label(withBuddy(named('lyricist'))).isShowingOnScreen()
        self.lineEdit(named('lyricist')).hasText(name)

    def changeLyricist(self, name):
        self.lineEdit(named('lyricist')).changeText(name)

    def showsComposer(self, name):
        self.label(withBuddy(named('composer'))).isShowingOnScreen()
        self.lineEdit(named('composer')).hasText(name)

    def changeComposer(self, name):
        self.lineEdit(named('composer')).changeText(name)

    def showsPublisher(self, name):
        self.label(withBuddy(named('publisher'))).isShowingOnScreen()
        self.lineEdit(named('publisher')).hasText(name)

    def changePublisher(self, name):
        self.lineEdit(named('publisher')).changeText(name)

    def showsIsrc(self, code):
        self.label(withBuddy(named('isrc'))).isShowingOnScreen()
        self.lineEdit(named('isrc')).hasText(code)

    def changeIsrc(self, code):
        self.lineEdit(named('isrc')).changeText(code)

    def showsIswc(self, code):
        self.label(withBuddy(named('iswc'))).isShowingOnScreen()
        edit = self.lineEdit(named('iswc'))
        edit.isDisabled()
        edit.hasText(code)

    def showsTags(self, tags):
        self.label(withBuddy(named('tags'))).isShowingOnScreen()
        self.lineEdit(named('tags')).hasText(tags)

    def changeTags(self, tags):
        self.lineEdit(named('tags')).changeText(tags)

    def showsLyrics(self, lyrics):
        self.label(withBuddy(named('lyrics'))).isShowingOnScreen()
        self.textEdit(named('lyrics')).hasPlainText(lyrics)

    def addLyrics(self, *lyrics):
        edit = self.textEdit(named('lyrics'))
        for lyric in lyrics:
            edit.addLine(lyric)
        edit.clearFocus()

    def showsLanguage(self, lang):
        self.label(withBuddy(named('languages'))).isShowingOnScreen()
        self.combobox(named('languages')).hasCurrentText(lang)

    def changeLanguage(self, lang):
        self.combobox(named('languages')).changeText(lang)

    def selectLanguage(self, lang):
        self.combobox(named('languages')).selectOption(lang)

    def showsPreviewTime(self, time):
        self.dateTimeEdit(named('preview-time')).hasTime(time)

    def showsBitrate(self, text):
        self.label(withBuddy(named('bitrate'))).isShowingOnScreen()
        self.label(named('bitrate')).hasText(text)

    def showsDuration(self, text):
        self.label(withBuddy(named('duration'))).isShowingOnScreen()
        self.label(named('duration')).hasText(text)

    def showsSoftwareNotice(self, notice):
        label = self.label(named('software-notice'))
        label.isShowingOnScreen()
        label.hasText(notice)