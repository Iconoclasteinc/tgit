# -*- coding: utf-8 -*-

from cute.matchers import named, withBuddy, showingOnScreen, withPixmapHeight, withPixmapWidth
from test.drivers import BaseDriver
from tgit.ui.track_edition_page import TrackEditionPage


def track_edition_page(parent):
    return TrackEditionPageDriver.findSingle(parent, TrackEditionPage, named('track-edition-page'), showingOnScreen())


class TrackEditionPageDriver(BaseDriver):
    def shows_metadata(self, **meta):
        for tag, value in meta.items():
            if tag == "track_title":
                self.showsTrackTitle(value)
            elif tag == 'lead_performer':
                self.shows_lead_performer(value)
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

    def change_metadata(self, **meta):
        for tag, value in meta.items():
            if tag == 'track_title':
                self.changeTrackTitle(value)
            elif tag == 'lead_performer':
                self.change_lead_performer(value)
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
        label.is_showing_on_screen()
        height, width = TrackEditionPage.ALBUM_COVER_SIZE
        label.hasPixmap(withPixmapHeight(height))
        label.hasPixmap(withPixmapWidth(width))

    def shows_album_lead_performer(self, name):
        label = self.label(named('album-lead-performer'))
        label.is_showing_on_screen()
        label.hasText(name)

    def showsAlbumTitle(self, title):
        label = self.label(named('album-title'))
        label.is_showing_on_screen()
        label.hasText(title)

    def showsAlbumLabel(self, name):
        label = self.label(named('record-label'))
        label.is_showing_on_screen()
        label.hasText(name)

    def showsTrackNumber(self, number):
        label = self.label(named('track-number'))
        label.is_showing_on_screen()
        label.hasText(number)

    def showsTrackTitle(self, trackTitle):
        self.label(withBuddy(named('track-title'))).is_showing_on_screen()
        self.lineEdit(named('track-title')).hasText(trackTitle)

    def changeTrackTitle(self, title):
        self.lineEdit(named('track-title')).changeText(title)

    def shows_lead_performer(self, name, disabled=False):
        self.label(withBuddy(named('lead-performer'))).is_showing_on_screen()
        edit = self.lineEdit(named('lead-performer'))
        edit.hasText(name)
        edit.is_disabled(disabled)

    def change_lead_performer(self, name):
        self.lineEdit(named('lead-performer')).changeText(name)

    def showsVersionInfo(self, versionInfo):
        self.label(withBuddy(named('version-info'))).is_showing_on_screen()
        self.lineEdit(named('version-info')).hasText(versionInfo)

    def changeVersionInfo(self, info):
        self.lineEdit(named('version-info')).changeText(info)

    def showsFeaturedGuest(self, name):
        self.label(withBuddy(named('featured-guest'))).is_showing_on_screen()
        self.lineEdit(named('featured-guest')).hasText(name)

    def changeFeaturedGuest(self, name):
        self.lineEdit(named('featured-guest')).changeText(name)

    def showsLyricist(self, name):
        self.label(withBuddy(named('lyricist'))).is_showing_on_screen()
        self.lineEdit(named('lyricist')).hasText(name)

    def changeLyricist(self, name):
        self.lineEdit(named('lyricist')).changeText(name)

    def showsComposer(self, name):
        self.label(withBuddy(named('composer'))).is_showing_on_screen()
        self.lineEdit(named('composer')).hasText(name)

    def changeComposer(self, name):
        self.lineEdit(named('composer')).changeText(name)

    def showsPublisher(self, name):
        self.label(withBuddy(named('publisher'))).is_showing_on_screen()
        self.lineEdit(named('publisher')).hasText(name)

    def changePublisher(self, name):
        self.lineEdit(named('publisher')).changeText(name)

    def showsIsrc(self, code):
        self.label(withBuddy(named('isrc'))).is_showing_on_screen()
        self.lineEdit(named('isrc')).hasText(code)

    def changeIsrc(self, code):
        self.lineEdit(named('isrc')).changeText(code)

    def showsIswc(self, code):
        self.label(withBuddy(named('iswc'))).is_showing_on_screen()
        edit = self.lineEdit(named('iswc'))
        edit.is_disabled()
        edit.hasText(code)

    def showsTags(self, tags):
        self.label(withBuddy(named('tags'))).is_showing_on_screen()
        self.lineEdit(named('tags')).hasText(tags)

    def changeTags(self, tags):
        self.lineEdit(named('tags')).changeText(tags)

    def showsLyrics(self, lyrics):
        self.label(withBuddy(named('lyrics'))).is_showing_on_screen()
        self.textEdit(named('lyrics')).hasPlainText(lyrics)

    def addLyrics(self, *lyrics):
        edit = self.textEdit(named('lyrics'))
        for lyric in lyrics:
            edit.addLine(lyric)
        edit.clearFocus()

    def showsLanguage(self, lang):
        self.label(withBuddy(named('languages'))).is_showing_on_screen()
        self.combobox(named('languages')).has_current_text(lang)

    def changeLanguage(self, lang):
        self.combobox(named('languages')).changeText(lang)

    def selectLanguage(self, lang):
        self.combobox(named('languages')).select_option(lang)

    def showsPreviewTime(self, time):
        self.dateTimeEdit(named('preview-time')).hasTime(time)

    def showsBitrate(self, text):
        self.label(withBuddy(named('bitrate'))).is_showing_on_screen()
        self.label(named('bitrate')).hasText(text)

    def showsDuration(self, text):
        self.label(withBuddy(named('duration'))).is_showing_on_screen()
        self.label(named('duration')).hasText(text)

    def showsSoftwareNotice(self, notice):
        label = self.label(named('software-notice'))
        label.is_showing_on_screen()
        label.hasText(notice)
