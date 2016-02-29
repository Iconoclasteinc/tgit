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
from PyQt5.QtCore import Qt, pyqtSignal, QDate
from PyQt5.QtWidgets import QWidget, QApplication, QMenu

from tgit.album import AlbumListener
from tgit.auth import Permission
from tgit.cheddar import AuthenticationError, InsufficientInformationError, PermissionDeniedError
from tgit.countries import COUNTRIES
from tgit.signal import MultiSubscription
from tgit.ui.closeable import Closeable
from tgit.ui.helpers import image
from tgit.ui.helpers.ui_file import UIFile

ISO_8601_FORMAT = "yyyy-MM-dd"


def make_album_edition_page(album, session, select_picture, select_identity, review_assignation,
                            show_isni_assignation_failed, show_cheddar_connection_failed,
                            show_cheddar_authentication_failed, show_permission_denied, **handlers):
    page = AlbumEditionPage(select_picture=select_picture,
                            select_identity=select_identity,
                            review_assignation=review_assignation,
                            show_isni_assignation_failed=show_isni_assignation_failed,
                            show_cheddar_connection_failed=show_cheddar_connection_failed,
                            show_cheddar_authentication_failed=show_cheddar_authentication_failed,
                            show_permission_denied=show_permission_denied)

    for name, handler in handlers.items():
        getattr(page, name)(handler)

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

    _picture = None
    _isni_lookup = False
    _isni_assign = False
    _metadata_changed = lambda: None

    FRONT_COVER_SIZE = 200, 200

    def __init__(self, select_picture, select_identity, review_assignation,
                 show_isni_assignation_failed, show_cheddar_connection_failed, show_cheddar_authentication_failed,
                 show_permission_denied):
        super().__init__()
        self._show_cheddar_authentication_failed = show_cheddar_authentication_failed
        self._review_assignation = review_assignation
        self._show_cheddar_connection_failed = show_cheddar_connection_failed
        self._show_isni_assignation_failed = show_isni_assignation_failed
        self._show_permission_denied = show_permission_denied
        self._select_identity = select_identity
        self._select_picture = select_picture
        self._setup_ui()

    def _setup_ui(self):
        self._load(":/ui/album_page.ui")
        self._fill_with_countries(self._main_artist_region)

        menu = QMenu()
        menu.addAction(self._main_artist_isni_assign_action)
        self._main_artist_isni_actions_button.setMenu(menu)

        def empty_main_artist():
            self._main_artist.setText("")
            self._main_artist_isni.setText("")
            self._main_artist_region.setCurrentText("")

        self._compilation.clicked.connect(self._update_isni_menu)
        self._compilation.clicked.connect(empty_main_artist)
        self._main_artist.textChanged.connect(self._update_isni_menu)

    @staticmethod
    def _fill_with_countries(combobox):
        for code, name in sorted(COUNTRIES.items(), key=operator.itemgetter(1)):
            combobox.addItem(name, code)
        combobox.insertItem(0, "")
        combobox.setCurrentIndex(0)

    def on_select_picture(self, on_select_picture):
        self._select_picture_button.clicked.connect(lambda: self._select_picture(on_select_picture))

    def on_isni_changed(self, on_isni_changed):
        self._main_artist_isni.editingFinished.connect(
            lambda: on_isni_changed(self._main_artist.text(), self._main_artist_isni.text()))

    def on_isni_local_lookup(self, on_isni_local_lookup):
        def update_main_artist_isni(main_artist):
            self._main_artist_isni.setText(on_isni_local_lookup(main_artist))

        self._main_artist.textEdited.connect(update_main_artist_isni)

    def on_isni_lookup(self, on_isni_lookup):
        def start_waiting():
            QApplication.setOverrideCursor(Qt.WaitCursor)
            try:
                on_isni_lookup(self._main_artist.text(), on_lookup_success)
            except requests.ConnectionError:
                self._show_cheddar_connection_failed()
            except AuthenticationError:
                self._show_cheddar_authentication_failed()
            except PermissionDeniedError:
                self._show_permission_denied()
            finally:
                QApplication.restoreOverrideCursor()

        def on_lookup_success(identities):
            self._select_identity(identities, on_identity_selected)
            QApplication.restoreOverrideCursor()

        def on_identity_selected(identity):
            self._main_artist_isni.setFocus(Qt.OtherFocusReason)
            self._main_artist_isni.setText(identity.id)

        self._main_artist_isni_actions_button.clicked.connect(start_waiting)

    def on_isni_assign(self, on_isni_assign):
        def start_waiting(main_artist_type):
            QApplication.setOverrideCursor(Qt.WaitCursor)
            try:
                on_isni_assign(main_artist_type, on_assign_success)
            except requests.ConnectionError:
                self._show_cheddar_connection_failed()
            except AuthenticationError:
                self._show_cheddar_authentication_failed()
            except InsufficientInformationError as e:
                self._show_isni_assignation_failed(str(e))
            finally:
                QApplication.restoreOverrideCursor()

        def on_assign_success(identity):
            self._main_artist_isni.setFocus(Qt.OtherFocusReason)
            self._main_artist_isni.setText(identity.id)
            QApplication.restoreOverrideCursor()

        self._main_artist_isni_assign_action.triggered.connect(lambda _: self._review_assignation(start_waiting))

    def on_remove_picture(self, on_remove_picture):
        self._remove_picture_button.clicked.connect(lambda _: on_remove_picture())

    def on_metadata_changed(self, handler):
        def handle(entry, musicians=None):
            handler(**self._metadata(musicians, entry))

        self._musician_table_container.on_musician_changed(lambda musicians: handle("guest_performers", musicians))
        self._release_time.dateChanged.connect(lambda: handle("release_time"))
        self._title.editingFinished.connect(lambda: handle("release_name"))
        self._compilation.clicked.connect(lambda: handle("compilation"))
        self._main_artist.editingFinished.connect(lambda: handle("lead_performer"))
        self._main_artist_region.activated.connect(lambda: handle("lead_performer_region"))
        self._label_name.editingFinished.connect(lambda: handle("label_name"))
        self._catalog_number.editingFinished.connect(lambda: handle("catalog_number"))
        self._barcode.editingFinished.connect(lambda: handle("upc"))

    def albumStateChanged(self, album):
        self.display(album)

    def user_changed(self, user):
        self._isni_lookup = user.has_permission(Permission.lookup_isni)
        self._isni_assign = user.has_permission(Permission.assign_isni)
        self._update_isni_menu()

    def display(self, album):
        if album.main_cover is not self._picture or album.main_cover is None:
            self._front_cover.setPixmap(image.scale(album.main_cover, *self.FRONT_COVER_SIZE))
            self._picture = album.main_cover
        self._title.setText(album.release_name)
        self._compilation.setChecked(album.compilation is True)
        self._display_main_artist(album)
        self._display_region(album.lead_performer_region, self._main_artist_region)
        self._label_name.setText(album.label_name)
        self._catalog_number.setText(album.catalog_number)
        self._barcode.setText(album.upc)
        self._release_time.setDate(QDate.fromString(album.release_time, ISO_8601_FORMAT))
        self._musician_table_container.display(album.guest_performers or [])

        identities = album.isnis or {}
        self._main_artist_isni.setText(identities[album.lead_performer] if album.lead_performer in identities else None)

    @staticmethod
    def _display_region(region, combobox):
        combobox.setCurrentText(COUNTRIES[region[0]]) if region else combobox.setCurrentIndex(0)

    def _display_main_artist(self, album):
        # todo this should be set in the embedded metadata adapter and we should have a checkbox for various artists
        self._main_artist.setText(album.compilation and self.tr("Various Artists") or album.lead_performer)

        disable_main_artist = album.compilation is True
        self._main_artist.setDisabled(disable_main_artist)
        self._main_artist_caption.setDisabled(disable_main_artist)
        self._main_artist_isni.setDisabled(disable_main_artist)
        self._main_artist_isni_caption.setDisabled(disable_main_artist)
        self._main_artist_region.setDisabled(disable_main_artist)
        self._main_artist_region_caption.setDisabled(disable_main_artist)

    def _metadata(self, musicians, *keys):
        all_values = dict(release_name=self._title.text(),
                          compilation=self._compilation.isChecked(),
                          lead_performer=self._main_artist.text(),
                          lead_performer_region=self._get_country_code_from_combo(self._main_artist_region),
                          guest_performers=musicians,
                          label_name=self._label_name.text(),
                          catalog_number=self._catalog_number.text(),
                          upc=self._barcode.text(),
                          release_time=self._release_time.date().toString(ISO_8601_FORMAT))

        if len(keys) == 0:
            return all_values

        keys_to_retrieve = [k for k in keys]
        if "compilation" not in keys_to_retrieve:
            keys_to_retrieve.append("compilation")

        if "lead_performer" not in keys_to_retrieve:
            keys_to_retrieve.append("lead_performer")

        return {k: all_values.get(k, None) for k in keys_to_retrieve}

    @staticmethod
    def _get_country_code_from_combo(combo):
        return (combo.currentData(),) if combo.currentIndex() > 0 else None

    def _update_isni_menu(self):
        def _is_blank(text):
            return not text or text.strip() == ""

        can_lookup_or_assign = not self._compilation.isChecked() and not _is_blank(self._main_artist.text())
        self._main_artist_isni_actions_button.setEnabled(self._isni_lookup and can_lookup_or_assign)
        self._main_artist_isni_assign_action.setEnabled(self._isni_assign and can_lookup_or_assign)


class MusicianTable(QWidget, UIFile):
    _on_musician_changed = lambda _: None

    def __init__(self, *__args):
        super().__init__(*__args)
        self._load(":/ui/musician_table.ui")
        self._add_musician_button.clicked.connect(lambda: self._add_musician_row())

    def display(self, musicians):
        if self._is_empty():
            for musician in musicians:
                self._add_musician_row(musician)

    def on_musician_changed(self, on_musician_changed):
        self._on_musician_changed = on_musician_changed

    def _is_empty(self):
        return self._musician_table.count() == 0

    def _add_musician_row(self, musician=(None, None)):
        self._musician_table.addWidget(
            make_musician_row(index=self._musician_table.count(),
                              musician=musician,
                              on_musician_changed=lambda: self._on_musician_changed(self._musicians),
                              on_musician_removed=lambda: self._on_musician_changed(self._musicians)))

    @property
    def _musicians(self):
        musicians = []
        for index in range(self._musician_table.count()):
            if self._row_is_empty(index):
                continue

            musicians.append(self._musician_table.itemAt(index).widget().musician)

        return musicians

    def _row_is_empty(self, index):
        return self._musician_table.itemAt(index) is None


def make_musician_row(index, on_musician_changed, on_musician_removed, musician):
    row = MusicianRow(index)
    row.musician_removed.connect(on_musician_removed)
    row.musician_changed.connect(on_musician_changed)
    row.display(*musician)

    return row


class MusicianRow(QWidget, UIFile):
    musician_removed = pyqtSignal()
    musician_changed = pyqtSignal()

    def __init__(self, index):
        super().__init__()
        self._load(":/ui/musician_row.ui")
        self.setObjectName("{}_{}".format(self.objectName(), index))
        self._remove_musician_button.clicked.connect(self._remove)
        self._instrument.editingFinished.connect(self._musician_changed)
        self._musician_name.editingFinished.connect(self._musician_changed)

    def display(self, instrument, musician_name):
        self._instrument.setText(instrument)
        self._musician_name.setText(musician_name)

    @property
    def musician(self):
        return self._instrument.text(), self._musician_name.text()

    def _remove(self):
        self.setParent(None)
        self.close()
        self.musician_removed.emit()

    def _musician_changed(self):
        if self._instrument.text() and self._musician_name.text():
            self.musician_changed.emit()
