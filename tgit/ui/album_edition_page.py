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

from PyQt5.QtCore import Qt, pyqtSignal, QDate
from PyQt5.QtWidgets import QWidget

from .helpers import image, formatting
from tgit.album import AlbumListener
from tgit.genres import GENRES
from tgit.auth import Permission
from tgit.signal import MultiSubscription
from tgit.ui.closeable import Closeable
from tgit.ui.helpers.ui_file import UIFile

ISO_8601_FORMAT = "yyyy-MM-dd"


def make_album_edition_page(album, session, edit_performers, select_picture, **handlers):
    page = AlbumEditionPage(select_picture=select_picture, edit_performers=edit_performers, **handlers)

    subscriptions = MultiSubscription()
    subscriptions.add(session.user_signed_in.subscribe(page.user_changed))
    subscriptions.add(session.user_signed_out.subscribe(lambda user: page.user_changed(session.current_user)))
    page.closed.connect(lambda: subscriptions.cancel())

    album.addAlbumListener(page)
    page.closed.connect(lambda: album.removeAlbumListener(page))

    page.user_changed(session.current_user)
    page.display(album)
    return page


@Closeable
class AlbumEditionPage(QWidget, UIFile, AlbumListener):
    closed = pyqtSignal()
    remove_picture = pyqtSignal()
    lookup_isni = pyqtSignal()
    clear_isni = pyqtSignal()
    assign_isni = pyqtSignal()
    metadata_changed = pyqtSignal(dict)

    _picture = None
    _isni_lookup = False

    FRONT_COVER_SIZE = 350, 350

    def __init__(self, edit_performers, select_picture, **handlers):
        super().__init__()
        self._select_picture = select_picture
        self._edit_performers = edit_performers
        self._setup_ui()

        for name, handler in handlers.items():
            getattr(self, name)(handler)

    def _setup_ui(self):
        self._load(":/ui/album_page.ui")
        self._disable_mac_focus_frame()

        # picture box
        self.front_cover.setFixedSize(*self.FRONT_COVER_SIZE)
        self.remove_picture_button.clicked.connect(lambda pressed: self.remove_picture.emit())

        # date box
        self.release_time.dateChanged.connect(lambda: self.metadata_changed.emit(self.metadata("release_time")))
        self.digital_release_time.dateChanged.connect(
            lambda: self.metadata_changed.emit(self.metadata("digital_release_time")))
        self.original_release_time.dateChanged.connect(
            lambda: self.metadata_changed.emit(self.metadata("original_release_time")))
        self.recording_time.dateChanged.connect(lambda: self.metadata_changed.emit(self.metadata("recording_time")))

        # album box
        self.release_name.editingFinished.connect(lambda: self.metadata_changed.emit(self.metadata("release_name")))
        self.lookup_isni_button.clicked.connect(lambda pressed: self.lookup_isni.emit())
        self.assign_isni_button.clicked.connect(lambda: self.assign_isni.emit())
        self.compilation.clicked.connect(lambda: self.metadata_changed.emit(self.metadata("compilation")))
        self.compilation.clicked.connect(self._update_isni_lookup_button)
        self.lead_performer.editingFinished.connect(lambda: self.metadata_changed.emit(self.metadata("lead_performer")))
        self.lead_performer.textChanged.connect(self._update_isni_lookup_button)
        self.clear_isni_button.clicked.connect(lambda: self.clear_isni.emit())
        self.clear_isni_button.clicked.connect(lambda: self.release_time.calendarWidget().show())
        self.add_guest_performers_button.clicked.connect(lambda: self._edit_performers(self._update_guest_performers))
        self.guest_performers.textChanged.connect(lambda: self.metadata_changed.emit(self.metadata("guest_performers")))

        # record
        self.label_name.editingFinished.connect(lambda: self.metadata_changed.emit(self.metadata("label_name")))
        self.catalog_number.editingFinished.connect(lambda: self.metadata_changed.emit(self.metadata("catalog_number")))
        self.barcode.editingFinished.connect(lambda: self.metadata_changed.emit(self.metadata("upc")))
        self.media_type.editingFinished.connect(lambda: self.metadata_changed.emit(self.metadata("media_type")))
        self.release_type.editingFinished.connect(lambda: self.metadata_changed.emit(self.metadata("release_type")))
        self.comments.editingFinished.connect(lambda: self.metadata_changed.emit(self.metadata("comments")))

        # recording
        self.recording_studios.editingFinished.connect(
            lambda: self.metadata_changed.emit(self.metadata("recording_studios")))
        self.producer.editingFinished.connect(lambda: self.metadata_changed.emit(self.metadata("producer")))
        self.mixer.editingFinished.connect(lambda: self.metadata_changed.emit(self.metadata("mixer")))
        self.genre.addItems(sorted(GENRES))
        self.genre.activated.connect(lambda: self.metadata_changed.emit(self.metadata("primary_style")))
        self.genre.lineEdit().textEdited.connect(
            lambda: self.metadata_changed.emit(self.metadata("primary_style")))

    def on_select_picture(self, on_select_picture):
        self.select_picture_button.clicked.connect(lambda: self._select_picture(on_select_picture))

    def _update_guest_performers(self, performers):
        self.guest_performers.setText(formatting.toPeopleList(performers))

    def albumStateChanged(self, album):
        self.display(album)

    def user_changed(self, user):
        self._isni_lookup = user.has_permission(Permission.isni_lookup)
        self._update_isni_lookup_button()

    def display(self, album):
        if album.mainCover is not self._picture or album.mainCover is None:
            self.front_cover.setPixmap(image.scale(album.mainCover, *self.FRONT_COVER_SIZE))
            self._picture = album.mainCover
        self.release_name.setText(album.release_name)
        self.compilation.setChecked(album.compilation is True)
        self._display_lead_performer(album)
        self.isni.setText(album.isni)
        self.guest_performers.setText(formatting.toPeopleList(album.guest_performers))
        self.label_name.setText(album.label_name)
        self.catalog_number.setText(album.catalog_number)
        self.barcode.setText(album.upc)
        self.comments.setPlainText(album.comments)
        self.release_time.setDate(QDate.fromString(album.release_time, ISO_8601_FORMAT))
        self.recording_time.setDate(QDate.fromString(album.recording_time, ISO_8601_FORMAT))
        self.recording_studios.setText(album.recording_studios)
        self.producer.setText(album.producer)
        self.mixer.setText(album.mixer)
        self.genre.setEditText(album.primary_style)

    def _display_lead_performer(self, album):
        # todo this should be set in the embedded metadata adapter and we should have a checkbox for various artists
        self.lead_performer.setText(album.compilation and self.tr("Various Artists") or album.lead_performer)
        self.lead_performer.setDisabled(album.compilation is True)

    def metadata(self, *keys):
        all_values = dict(release_name=self.release_name.text(),
                          compilation=self.compilation.isChecked(),
                          lead_performer=self.lead_performer.text(),
                          isni=self.isni.text(),
                          guest_performers=formatting.fromPeopleList(self.guest_performers.text()),
                          label_name=self.label_name.text(),
                          catalog_number=self.catalog_number.text(),
                          upc=self.barcode.text(),
                          comments=self.comments.toPlainText(),
                          recording_time=self.recording_time.date().toString(ISO_8601_FORMAT),
                          release_time=self.release_time.date().toString(ISO_8601_FORMAT),
                          recording_studios=self.recording_studios.text(),
                          producer=self.producer.text(),
                          mixer=self.mixer.text(),
                          primary_style=self.genre.currentText())

        if len(keys) == 0:
            return all_values

        keys_to_retrieve = [k for k in keys]
        if "compilation" not in keys_to_retrieve:
            keys_to_retrieve.append("compilation")

        if "lead_performer" not in keys_to_retrieve:
            keys_to_retrieve.append("lead_performer")

        return {k: all_values.get(k, None) for k in keys_to_retrieve}

    def _disable_mac_focus_frame(self):
        for child in self.findChildren(QWidget):
            child.setAttribute(Qt.WA_MacShowFocusRect, False)

    def _update_isni_lookup_button(self):
        self.lookup_isni_button.setEnabled(
            self._isni_lookup and not self.compilation.isChecked() and not is_blank(self.lead_performer.text()))


def is_blank(text):
    return not text or text.strip() == ""
