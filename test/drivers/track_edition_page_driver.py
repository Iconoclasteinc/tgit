# -*- coding: utf-8 -*-

from cute.matchers import named, with_buddy, showing_on_screen, with_pixmap_height, with_pixmap_width
from tgit.ui.track_edition_page import TrackEditionPage
from ._screen_driver import ScreenDriver


def track_edition_page(parent):
    return TrackEditionPageDriver.find_single(parent, TrackEditionPage, named('track-edition-page'), showing_on_screen())


class TrackEditionPageDriver(ScreenDriver):
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
        label.has_pixmap(with_pixmap_height(height))
        label.has_pixmap(with_pixmap_width(width))

    def shows_album_lead_performer(self, name):
        label = self.label(named('album-lead-performer'))
        label.is_showing_on_screen()
        label.has_text(name)

    def showsAlbumTitle(self, title):
        label = self.label(named('album-title'))
        label.is_showing_on_screen()
        label.has_text(title)

    def showsAlbumLabel(self, name):
        label = self.label(named('record-label'))
        label.is_showing_on_screen()
        label.has_text(name)

    def showsTrackNumber(self, number):
        label = self.label(named('track-number'))
        label.is_showing_on_screen()
        label.has_text(number)

    def showsTrackTitle(self, trackTitle):
        self.label(with_buddy(named('track-title'))).is_showing_on_screen()
        self.lineEdit(named('track-title')).has_text(trackTitle)

    def changeTrackTitle(self, title):
        self.lineEdit(named('track-title')).change_text(title)

    def shows_lead_performer(self, name, disabled=False):
        self.label(with_buddy(named('lead-performer'))).is_showing_on_screen()
        edit = self.lineEdit(named('lead-performer'))
        edit.has_text(name)
        edit.is_disabled(disabled)

    def change_lead_performer(self, name):
        self.lineEdit(named('lead-performer')).change_text(name)

    def showsVersionInfo(self, versionInfo):
        self.label(with_buddy(named('version-info'))).is_showing_on_screen()
        self.lineEdit(named('version-info')).has_text(versionInfo)

    def changeVersionInfo(self, info):
        self.lineEdit(named('version-info')).change_text(info)

    def showsFeaturedGuest(self, name):
        self.label(with_buddy(named('featured-guest'))).is_showing_on_screen()
        self.lineEdit(named('featured-guest')).has_text(name)

    def changeFeaturedGuest(self, name):
        self.lineEdit(named('featured-guest')).change_text(name)

    def showsLyricist(self, name):
        self.label(with_buddy(named('lyricist'))).is_showing_on_screen()
        self.lineEdit(named('lyricist')).has_text(name)

    def changeLyricist(self, name):
        self.lineEdit(named('lyricist')).change_text(name)

    def showsComposer(self, name):
        self.label(with_buddy(named('composer'))).is_showing_on_screen()
        self.lineEdit(named('composer')).has_text(name)

    def changeComposer(self, name):
        self.lineEdit(named('composer')).change_text(name)

    def showsPublisher(self, name):
        self.label(with_buddy(named('publisher'))).is_showing_on_screen()
        self.lineEdit(named('publisher')).has_text(name)

    def changePublisher(self, name):
        self.lineEdit(named('publisher')).change_text(name)

    def showsIsrc(self, code):
        self.label(with_buddy(named('isrc'))).is_showing_on_screen()
        self.lineEdit(named('isrc')).has_text(code)

    def changeIsrc(self, code):
        self.lineEdit(named('isrc')).change_text(code)

    def showsIswc(self, code):
        self.label(with_buddy(named('iswc'))).is_showing_on_screen()
        edit = self.lineEdit(named('iswc'))
        edit.is_disabled()
        edit.has_text(code)

    def showsTags(self, tags):
        self.label(with_buddy(named('tags'))).is_showing_on_screen()
        self.lineEdit(named('tags')).has_text(tags)

    def changeTags(self, tags):
        self.lineEdit(named('tags')).change_text(tags)

    def showsLyrics(self, lyrics):
        self.label(with_buddy(named('lyrics'))).is_showing_on_screen()
        self.textEdit(named('lyrics')).has_plain_text(lyrics)

    def addLyrics(self, *lyrics):
        edit = self.textEdit(named('lyrics'))
        for lyric in lyrics:
            edit.add_line(lyric)
        edit.clear_focus()

    def showsLanguage(self, lang):
        self.label(with_buddy(named('languages'))).is_showing_on_screen()
        self.combobox(named('languages')).has_current_text(lang)

    def changeLanguage(self, lang):
        self.combobox(named('languages')).change_text(lang)

    def selectLanguage(self, lang):
        self.combobox(named('languages')).select_option(lang)

    def showsPreviewTime(self, time):
        self.dateTimeEdit(named('preview-time')).has_time(time)

    def showsBitrate(self, text):
        self.label(with_buddy(named('bitrate'))).is_showing_on_screen()
        self.label(named('bitrate')).has_text(text)

    def showsDuration(self, text):
        self.label(with_buddy(named('duration'))).is_showing_on_screen()
        self.label(named('duration')).has_text(text)

    def showsSoftwareNotice(self, notice):
        label = self.label(named('software-notice'))
        label.is_showing_on_screen()
        label.has_text(notice)
