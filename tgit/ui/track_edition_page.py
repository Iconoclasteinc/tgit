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

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget

from tgit.album import AlbumListener
from tgit.countries import COUNTRIES
from tgit.genres import GENRES
from tgit.languages import LANGUAGES
from tgit.ui.closeable import Closeable
from tgit.ui.helpers import image, formatting
from tgit.ui.helpers.ui_file import UIFile


def make_track_edition_page(album, track, on_track_changed):
    page = TrackEditionPage()

    page.metadata_changed.connect(lambda metadata: on_track_changed(**metadata))

    subscription = track.metadata_changed.subscribe(page.display_track)
    page.closed.connect(lambda: subscription.cancel())
    album.addAlbumListener(page)
    page.closed.connect(lambda: album.removeAlbumListener(page))

    page.display(album=album, track=track)
    return page


@Closeable
class TrackEditionPage(QWidget, UIFile, AlbumListener):
    closed = pyqtSignal()

    # TODO move from signal to on_metadata_changed handler
    metadata_changed = pyqtSignal(dict)

    ALBUM_COVER_SIZE = 50, 50
    DURATION_FORMAT = "mm:ss"

    _cover = None

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        self._load(":/ui/track_page.ui")
        self._disable_mac_focus_frame()
        self._disable_teaser_fields()

        self._genre.addItems(sorted(GENRES))
        self._language.addItems(sorted(LANGUAGES))
        self._fill_with_countries(self._production_company_region)
        self._fill_with_countries(self._recording_studio_region)

        def emit_metadata_changed():
            self.metadata_changed.emit(self.metadata)

        self._track_title.editingFinished.connect(emit_metadata_changed)
        self._lead_performer.editingFinished.connect(emit_metadata_changed)
        self._version.editingFinished.connect(emit_metadata_changed)
        self._featured_guest.editingFinished.connect(emit_metadata_changed)
        self._lyricist.editingFinished.connect(emit_metadata_changed)
        self._composer.editingFinished.connect(emit_metadata_changed)
        self._publisher.editingFinished.connect(emit_metadata_changed)
        self._isrc.editingFinished.connect(emit_metadata_changed)
        self._iswc.editingFinished.connect(emit_metadata_changed)
        self._tags.editingFinished.connect(emit_metadata_changed)

        self._lyrics.editingFinished.connect(emit_metadata_changed)
        self._language.activated.connect(emit_metadata_changed)
        self._language.lineEdit().textEdited.connect(emit_metadata_changed)

        self._recording_studio.editingFinished.connect(emit_metadata_changed)
        self._recording_studio_region.activated.connect(emit_metadata_changed)
        self._music_producer.editingFinished.connect(emit_metadata_changed)
        self._production_company.editingFinished.connect(emit_metadata_changed)
        self._production_company_region.activated.connect(emit_metadata_changed)
        self._mixer.editingFinished.connect(emit_metadata_changed)
        self._genre.activated.connect(emit_metadata_changed)
        self._genre.lineEdit().textEdited.connect(emit_metadata_changed)

    def albumStateChanged(self, album):
        self.display(album=album)

    def display(self, album=None, track=None):
        if album:
            self._display_album(album)
        if track:
            self.display_track(track)

    def _display_album(self, album):
        self._display_album_cover(album.main_cover)
        self._album_title.setText(album.release_name)
        self._album_lead_performer.setText(album.compilation and self.tr("Various Artists") or album.lead_performer)
        self._lead_performer.setEnabled(album.compilation is True)
        self._lead_performer_caption.setEnabled(album.compilation is True)

    def display_track(self, track):
        self._track_number.setText(self.tr("Track {0} of {1}").format(track.track_number, track.total_tracks))
        self._track_title.setText(track.track_title)
        self._lead_performer.setText(track.lead_performer)
        self._version.setText(track.versionInfo)
        self._duration.setText(formatting.to_duration(track.duration))
        self._bitrate.setText("{0} kbps".format(formatting.in_kbps(track.bitrate)))
        self._featured_guest.setText(track.featuredGuest)
        self._lyricist.setText(track.lyricist)
        self._composer.setText(track.composer)
        self._publisher.setText(track.publisher)
        self._isrc.setText(track.isrc)
        self._iswc.setText(track.iswc)
        self._tags.setText(track.labels)
        self._lyrics.setPlainText(track.lyrics)
        self._language.setEditText(track.language)
        self._software_notice.setText(self._compose_software_notice(track))

        self._recording_studio.setText(track.recording_studio)
        self._display_region(track.recording_studio_region, self._recording_studio_region)
        self._music_producer.setText(track.music_producer)
        self._production_company.setText(track.production_company)
        self._display_region(track.production_company_region, self._production_company_region)
        self._mixer.setText(track.mixer)
        self._genre.setEditText(track.primary_style)

    @staticmethod
    def _display_region(region, combobox):
        if region:
            combobox.setCurrentText(COUNTRIES[region[0]])

    def _display_album_cover(self, picture):
        # Cache the cover image to avoid recomputing the image each time the screen updates
        if self._cover is not picture:
            self._cover = picture
            self._album_cover.setPixmap(image.scale(self._cover, *self.ALBUM_COVER_SIZE))

    def _compose_software_notice(self, track):
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
    def metadata(self):
        return dict(track_title=self._track_title.text(),
                    lead_performer=self._lead_performer.text(),
                    versionInfo=self._version.text(),
                    featuredGuest=self._featured_guest.text(),
                    lyricist=self._lyricist.text(),
                    composer=self._composer.text(),
                    publisher=self._publisher.text(),
                    isrc=self._isrc.text(),
                    iswc=self._iswc.text(),
                    labels=self._tags.text(),
                    lyrics=self._lyrics.toPlainText(),
                    language=self._language.currentText(),
                    recording_studio=self._recording_studio.text(),
                    recording_studio_region=self._get_country_code_from_combo(self._recording_studio_region),
                    music_producer=self._music_producer.text(),
                    production_company=self._production_company.text(),
                    production_company_region=self._get_country_code_from_combo(self._production_company_region),
                    mixer=self._mixer.text(),
                    primary_style=self._genre.currentText())

    def _disable_mac_focus_frame(self):
        for child in self.findChildren(QWidget):
            child.setAttribute(Qt.WA_MacShowFocusRect, False)

    def _disable_teaser_fields(self):
        self._preview_time.setDisabled(True)
        self._preview_time_caption.setDisabled(True)

    @staticmethod
    def _fill_with_countries(combobox):
        for code, name in sorted(COUNTRIES.items(), key=operator.itemgetter(1)):
            combobox.addItem(name, code)
        combobox.insertItem(0, "")
        combobox.setCurrentIndex(0)

    @staticmethod
    def _get_country_code_from_combo(combo):
        return (combo.currentData(),) if combo.currentIndex() > 0 else None
