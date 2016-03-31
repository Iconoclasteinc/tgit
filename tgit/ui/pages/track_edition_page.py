# -*- coding: utf-8 -*-
#
# TGiT, Music Tagger for Professionals
# Copyright (C) 2013 Iconoclaste Musique Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
import operator

from PyQt5.QtCore import pyqtSignal, QDate
from PyQt5.QtWidgets import QWidget

from tgit import imager
from tgit.album import AlbumListener
from tgit.countries import COUNTRIES
from tgit.genres import GENRES
from tgit.languages import LANGUAGES
from tgit.ui import pixmap
from tgit.ui.closeable import Closeable
from tgit.ui.helpers import formatting
from tgit.ui.helpers.ui_file import UIFile
from tgit.ui.pages.project_edition_page import ISO_8601_FORMAT


def make_track_edition_page(album, track, **handlers):
    page = TrackEditionPage()
    for name, handler in handlers.items():
        getattr(page, name)(handler)

    subscription = track.metadata_changed.subscribe(page.display_track)
    page.closed.connect(lambda: subscription.cancel())
    album.addAlbumListener(page)
    page.closed.connect(lambda: album.removeAlbumListener(page))

    page.display(album=album, track=track)
    return page


@Closeable
class TrackEditionPage(QWidget, UIFile, AlbumListener):
    closed = pyqtSignal()

    ALBUM_COVER_SIZE = 75, 75
    DURATION_FORMAT = "mm:ss"

    _cover = None

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        def fill_with_countries(combobox):
            for code, name in sorted(COUNTRIES.items(), key=operator.itemgetter(1)):
                combobox.addItem(name, code)
            combobox.insertItem(0, "")
            combobox.setCurrentIndex(0)

        def fill_with_languages(combobox):
            for code, name in sorted(LANGUAGES.items(), key=lambda item: self.tr(item[1])):
                combobox.addItem(self.tr(name), code)

        self._load(":/ui/track_page.ui")

        self._no_cover = pixmap.none(*self.ALBUM_COVER_SIZE)
        self._broken_cover = pixmap.broken(*self.ALBUM_COVER_SIZE)
        self._album_cover.setPixmap(self._no_cover)
        self._genre.addItems(sorted(GENRES))
        fill_with_languages(self._language)
        fill_with_countries(self._production_company_region)
        fill_with_countries(self._recording_studio_region)

    def albumStateChanged(self, album):
        self.display(album=album)

    def on_track_changed(self, handler):
        def handle(*_):
            handler(**self._metadata)

        self._track_title.editingFinished.connect(handle)
        self._main_artist.editingFinished.connect(handle)
        self._version.editingFinished.connect(handle)
        self._featured_guest.editingFinished.connect(handle)
        self._comments.editingFinished.connect(handle)
        self._lyricist.editingFinished.connect(handle)
        self._composer.editingFinished.connect(handle)
        self._publisher.editingFinished.connect(handle)
        self._isrc.editingFinished.connect(handle)
        self._iswc.editingFinished.connect(handle)
        self._tags.editingFinished.connect(handle)

        self._lyrics.editingFinished.connect(handle)
        self._language.activated.connect(handle)

        self._recording_studio.editingFinished.connect(handle)
        self._recording_studio_region.activated.connect(handle)
        self._recording_time.dateChanged.connect(handle)
        self._music_producer.editingFinished.connect(handle)
        self._production_company.editingFinished.connect(handle)
        self._production_company_region.activated.connect(handle)
        self._mixer.editingFinished.connect(handle)
        self._genre.activated.connect(handle)
        self._genre.lineEdit().textEdited.connect(handle)

    def on_isni_local_lookup(self, handler):
        self._lyricist.textEdited.connect(lambda text: self._lyricist_isni.setText(handler(text)))
        self._composer.textEdited.connect(lambda text: self._composer_isni.setText(handler(text)))
        self._publisher.textEdited.connect(lambda text: self._publisher_isni.setText(handler(text)))

    def on_ipi_local_lookup(self, handler):
        self._lyricist.textEdited.connect(lambda text: self._lyricist_ipi.setText(handler(text)))
        self._composer.textEdited.connect(lambda text: self._composer_ipi.setText(handler(text)))
        self._publisher.textEdited.connect(lambda text: self._publisher_ipi.setText(handler(text)))

    def on_ipi_changed(self, on_ipi_changed):
        def handler(name, ipi):
            if name:
                on_ipi_changed(name, ipi)

        self._lyricist_ipi.editingFinished.connect(lambda: handler(self._lyricist.text(), self._lyricist_ipi.text()))
        self._composer_ipi.editingFinished.connect(lambda: handler(self._composer.text(), self._composer_ipi.text()))
        self._publisher_ipi.editingFinished.connect(lambda: handler(self._publisher.text(), self._publisher_ipi.text()))

    def display(self, album=None, track=None):
        if track:
            self.display_track(track)
        if album:
            self._display_album(album)

    def _display_album(self, album):
        self._display_album_cover(album.main_cover)
        self._album_title.setText(album.release_name)
        if album.compilation:
            self._album_main_artist.setText(self.tr("Various Artists"))
        else:
            self._album_main_artist.setText(album.lead_performer)

        enable_main_artist = album.compilation is True
        self._main_artist.setEnabled(enable_main_artist)
        self._main_artist_caption.setEnabled(enable_main_artist)
        self._main_artist_info.setEnabled(enable_main_artist)
        self._main_artist_help.setEnabled(enable_main_artist)

        isnis = album.isnis or {}
        self._lyricist_isni.setText(isnis.get(self._lyricist.text()))
        self._composer_isni.setText(isnis.get(self._composer.text()))
        self._publisher_isni.setText(isnis.get(self._publisher.text()))

        ipis = album.ipis or {}
        self._lyricist_ipi.setText(ipis.get(self._lyricist.text()))
        self._composer_ipi.setText(ipis.get(self._composer.text()))
        self._publisher_ipi.setText(ipis.get(self._publisher.text()))

    def display_track(self, track):
        self._track_number.setText(self.tr("Track {0} of {1}").format(track.track_number, track.total_tracks))
        self._track_title.setText(track.track_title)
        self._main_artist.setText(track.lead_performer)
        self._version.setText(track.version_info)
        self._duration.setText(formatting.to_duration(track.duration))
        self._bitrate.setText("{0} kbps".format(formatting.in_kbps(track.bitrate)))
        self._featured_guest.setText(track.featured_guest)
        self._comments.setPlainText(track.comments)
        self._lyricist.setText(track.lyricist)
        self._composer.setText(track.composer)
        self._publisher.setText(track.publisher)
        self._isrc.setText(track.isrc)
        self._iswc.setText(track.iswc)
        self._tags.setText(track.labels)
        self._lyrics.setPlainText(track.lyrics)
        self._language.setCurrentText(self.tr(LANGUAGES[track.language or 'und']))
        self._software_notice.setText(self._compose_software_notice(track))

        self._recording_studio.setText(track.recording_studio)
        self._recording_time.setDate(QDate.fromString(track.recording_time, ISO_8601_FORMAT))
        self._display_region(track.recording_studio_region, self._recording_studio_region)
        self._music_producer.setText(track.music_producer)
        self._production_company.setText(track.production_company)
        self._display_region(track.production_company_region, self._production_company_region)
        self._mixer.setText(track.mixer)
        self._genre.setEditText(track.primary_style)

        isnis = track.album.isnis or {}
        self._lyricist_isni.setText(isnis.get(track.lyricist))
        self._composer_isni.setText(isnis.get(track.composer))
        self._publisher_isni.setText(isnis.get(track.publisher))

        ipis = track.album.ipis or {}
        self._lyricist_ipi.setText(ipis.get(track.lyricist))
        self._composer_ipi.setText(ipis.get(track.composer))
        self._publisher_ipi.setText(ipis.get(track.publisher))

    @staticmethod
    def _display_region(region, combobox):
        if region:
            combobox.setCurrentText(COUNTRIES[region[0]])

    def _display_album_cover(self, picture):
        # Cache the cover image to avoid recomputing the image each time the screen updates
        if self._cover is not picture:
            self._cover = picture
            self._album_cover.setPixmap(self._scale_cover(picture))

    def _scale_cover(self, picture):
        if not picture:
            return self._no_cover
        scaled_cover = pixmap.from_image(imager.scale(picture, *self.ALBUM_COVER_SIZE))
        return self._broken_cover if scaled_cover.isNull() else scaled_cover

    def _compose_software_notice(self, track):
        # noinspection PyBroadException
        try:
            date, time = formatting.as_local_date_time(track.tagging_time)
        except:
            date, time = None, None

        notice = ""
        if track.tagger and track.tagger_version:
            notice += self.tr(" with {0} v{1}").format(track.tagger, track.tagger_version)
        if date and time:
            notice += self.tr(" on {0} at {1}").format(date, time)

        if notice != "":
            notice = self.tr("Tagged") + notice

        return notice

    @property
    def _metadata(self):
        metadata = dict(track_title=self._track_title.text(),
                        version_info=self._version.text(),
                        featured_guest=self._featured_guest.text(),
                        comments=self._comments.toPlainText(),
                        composer=self._composer.text(),
                        publisher=self._publisher.text(),
                        isrc=self._isrc.text(),
                        iswc=self._iswc.text(),
                        labels=self._tags.text(),
                        lyrics=self._lyrics.toPlainText(),
                        lyricist=self._lyricist.text(),
                        language=self._language.currentData(),
                        recording_studio=self._recording_studio.text(),
                        recording_studio_region=self._get_country_code_from_combo(self._recording_studio_region),
                        recording_time=self._recording_time.date().toString(ISO_8601_FORMAT),
                        music_producer=self._music_producer.text(),
                        production_company=self._production_company.text(),
                        production_company_region=self._get_country_code_from_combo(self._production_company_region),
                        mixer=self._mixer.text(),
                        primary_style=self._genre.currentText())

        if self._main_artist.isEnabled():
            metadata["lead_performer"] = self._main_artist.text()

        return metadata

    @staticmethod
    def _get_country_code_from_combo(combo):
        return (combo.currentData(),) if combo.currentIndex() > 0 else None
