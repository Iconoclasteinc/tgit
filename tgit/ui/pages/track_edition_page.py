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

import requests
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QMenu, QApplication

from tgit.album import AlbumListener
from tgit.cheddar import AuthenticationError
from tgit.cheddar import InsufficientInformationError
from tgit.countries import COUNTRIES
from tgit.genres import GENRES
from tgit.languages import LANGUAGES
from tgit.ui.closeable import Closeable
from tgit.ui.helpers import image, formatting
from tgit.ui.helpers.ui_file import UIFile

QMENU_STYLESHEET = """
    QMenu {
        background-color: white;
    }

    QMenu::item::selected {
      color: black;
      background-color:#DDDDDD;
    }
"""


def make_track_edition_page(album, track, on_track_changed, review_assignation, show_isni_assignation_failed,
                            show_cheddar_connection_failed, show_cheddar_authentication_failed, **handlers):
    page = TrackEditionPage(review_assignation, show_isni_assignation_failed, show_cheddar_connection_failed,
                            show_cheddar_authentication_failed)
    for name, handler in handlers.items():
        getattr(page, name)(handler)

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

    def __init__(self, review_assignation, show_isni_assignation_failed, show_cheddar_connection_failed,
                 show_cheddar_authentication_failed):
        super().__init__()
        self._show_cheddar_authentication_failed = show_cheddar_authentication_failed
        self._show_cheddar_connection_failed = show_cheddar_connection_failed
        self._show_isni_assignation_failed = show_isni_assignation_failed
        self._review_assignation = review_assignation
        self._setup_ui()

    def _setup_ui(self):
        self._load(":/ui/track_page.ui")
        self._disable_mac_focus_frame()
        self._disable_teaser_fields()

        lyricist_menu = QMenu()
        lyricist_menu.setStyleSheet(QMENU_STYLESHEET)
        lyricist_menu.addAction(self._lyricist_isni_assign_action)
        self._lyricist_isni_actions_button.setMenu(lyricist_menu)

        composer_menu = QMenu()
        composer_menu.setStyleSheet(QMENU_STYLESHEET)
        composer_menu.addAction(self._composer_isni_assign_action)
        self._composer_isni_actions_button.setMenu(composer_menu)

        publisher_menu = QMenu()
        publisher_menu.setStyleSheet(QMENU_STYLESHEET)
        publisher_menu.addAction(self._publisher_isni_assign_action)
        self._publisher_isni_actions_button.setMenu(publisher_menu)

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

    def on_lyricist_isni_assign(self, handler):
        def start_waiting():
            QApplication.setOverrideCursor(Qt.WaitCursor)
            try:
                handler(on_assign_success)
            except requests.ConnectionError:
                self._show_cheddar_connection_failed()
            except AuthenticationError:
                self._show_cheddar_authentication_failed()
            except InsufficientInformationError as e:
                self._show_isni_assignation_failed(str(e))
            finally:
                QApplication.restoreOverrideCursor()

        def on_assign_success(identity):
            self._lyricist_isni.setFocus(Qt.OtherFocusReason)
            self._lyricist_isni.setText(identity.id)
            QApplication.restoreOverrideCursor()

        self._lyricist_isni_assign_action.triggered.connect(lambda _: self._review_assignation(start_waiting))

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
            self._album_lead_performer.setText(self.tr("Various Artists"))
        else:
            self._album_lead_performer.setText(album.lead_performer)
        self._lead_performer.setEnabled(album.compilation is True)
        self._lead_performer_caption.setEnabled(album.compilation is True)

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
        self._lead_performer.setText(track.lead_performer)
        self._version.setText(track.version_info)
        self._duration.setText(formatting.to_duration(track.duration))
        self._bitrate.setText("{0} kbps".format(formatting.in_kbps(track.bitrate)))
        self._featured_guest.setText(track.featured_guest)
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
            self._album_cover.setPixmap(image.scale(self._cover, *self.ALBUM_COVER_SIZE))

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
    def metadata(self):
        metadata = dict(track_title=self._track_title.text(),
                        version_info=self._version.text(),
                        featured_guest=self._featured_guest.text(),
                        composer=self._composer.text(),
                        publisher=self._publisher.text(),
                        isrc=self._isrc.text(),
                        iswc=self._iswc.text(),
                        labels=self._tags.text(),
                        lyrics=self._lyrics.toPlainText(),
                        lyricist=self._lyricist.text(),
                        language=self._language.currentText(),
                        recording_studio=self._recording_studio.text(),
                        recording_studio_region=self._get_country_code_from_combo(self._recording_studio_region),
                        music_producer=self._music_producer.text(),
                        production_company=self._production_company.text(),
                        production_company_region=self._get_country_code_from_combo(self._production_company_region),
                        mixer=self._mixer.text(),
                        primary_style=self._genre.currentText())

        if self._lead_performer.isEnabled():
            metadata["lead_performer"] = self._lead_performer.text()

        return metadata

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
