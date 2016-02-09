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

from PyQt5.QtGui import QIcon
import requests
from PyQt5.QtCore import Qt, pyqtSignal, QDate, QSize
from PyQt5.QtWidgets import QWidget, QApplication, QMenu, QLineEdit, QPushButton, QGridLayout, QLabel

from tgit.album import AlbumListener
from tgit.auth import Permission
from tgit.cheddar import AuthenticationError, InsufficientInformationError, PermissionDeniedError
from tgit.countries import COUNTRIES
from tgit.signal import MultiSubscription
from tgit.ui.closeable import Closeable
from tgit.ui.helpers import image, formatting
from tgit.ui.helpers.ui_file import UIFile

INSTRUMENT_COLUMN_INDEX = 0
PERFORMER_COLUMN_INDEX = 1
REMOVE_BUTTON_COLUMN_INDEX = 2
FIRST_PERFORMER_ROW_INDEX = 1
ISO_8601_FORMAT = "yyyy-MM-dd"
QMENU_STYLESHEET = """
    QMenu {
        background-color: white;
    }

    QMenu::item::selected {
      color: black;
      background-color:#DDDDDD;
    }
"""


def make_album_edition_page(album, session, edit_performers, select_picture, select_identity, review_assignation,
                            show_isni_assignation_failed, show_cheddar_connection_failed,
                            show_cheddar_authentication_failed, show_permission_denied, **handlers):
    page = AlbumEditionPage(select_picture=select_picture,
                            edit_artists=edit_performers,
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

    FRONT_COVER_SIZE = 138, 138

    def __init__(self, edit_artists, select_picture, select_identity, review_assignation,
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
        self._edit_artists = edit_artists
        self._setup_ui()

    def _setup_ui(self):
        self._load(":/ui/album_page.ui")
        self._disable_mac_focus_frame()

        self._fill_with_countries(self._main_artist_region)

        menu = QMenu()
        menu.addAction(self._main_artist_isni_assign_action)
        self._main_artist_isni_actions_button.setMenu(menu)

        self._compilation.clicked.connect(self._update_isni_menu)
        self._main_artist.textChanged.connect(self._update_isni_menu)
        self._add_artist_button.clicked.connect(lambda: self._edit_artists(self._update_artists))
        self._add_artist_button_2.clicked.connect(lambda _: self._build_artist_row())

    @staticmethod
    def _fill_with_countries(combobox):
        for code, name in sorted(COUNTRIES.items(), key=operator.itemgetter(1)):
            combobox.addItem(name, code)
        combobox.insertItem(0, "")
        combobox.setCurrentIndex(0)

    def on_select_picture(self, on_select_picture):
        self._front_cover.clicked.connect(lambda: self._select_picture(on_select_picture))

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
        def handle(entry):
            handler(**self._metadata(entry))

        self._release_time.dateChanged.connect(lambda: handle("release_time"))
        self._digital_release_time.dateChanged.connect(lambda: handle("digital_release_time"))
        self._original_release_time.dateChanged.connect(lambda: handle("original_release_time"))
        self._recording_time.dateChanged.connect(lambda: handle("recording_time"))
        self._release_name.editingFinished.connect(lambda: handle("release_name"))
        self._compilation.clicked.connect(lambda: handle("compilation"))
        self._main_artist.editingFinished.connect(lambda: handle("lead_performer"))
        self._main_artist_region.activated.connect(lambda: handle("lead_performer_region"))
        self._artists.textChanged.connect(lambda: handle("guest_performers"))
        self._label_name.editingFinished.connect(lambda: handle("label_name"))
        self._catalog_number.editingFinished.connect(lambda: handle("catalog_number"))
        self._barcode.editingFinished.connect(lambda: handle("upc"))
        self._media_type.editingFinished.connect(lambda: handle("media_type"))
        self._release_type.editingFinished.connect(lambda: handle("release_type"))
        self._comments.editingFinished.connect(lambda: handle("comments"))

    def _update_artists(self, artists):
        self._artists.setText(formatting.toPeopleList(artists))

    def albumStateChanged(self, album):
        self.display(album)

    def user_changed(self, user):
        self._isni_lookup = user.has_permission(Permission.lookup_isni)
        self._isni_assign = user.has_permission(Permission.assign_isni)
        if not self._isni_lookup:
            self._main_artist_isni_actions_button.setToolTip(self.tr("Please sign-in to activate ISNI lookup"))
        else:
            self._main_artist_isni_actions_button.setToolTip(None)
        self._update_isni_menu()

    def display(self, album):
        if album.main_cover is not self._picture or album.main_cover is None:
            self._front_cover.setIcon(QIcon(image.scale(album.main_cover, *self.FRONT_COVER_SIZE)))
            self._front_cover.setIconSize(QSize(*self.FRONT_COVER_SIZE))
            self._picture = album.main_cover
        self._release_name.setText(album.release_name)
        self._compilation.setChecked(album.compilation is True)
        self._display_main_artist(album)
        self._display_region(album.lead_performer_region, self._main_artist_region)
        self._artists.setText(formatting.toPeopleList(album.guest_performers))
        self._label_name.setText(album.label_name)
        self._catalog_number.setText(album.catalog_number)
        self._barcode.setText(album.upc)
        self._comments.setPlainText(album.comments)
        self._release_time.setDate(QDate.fromString(album.release_time, ISO_8601_FORMAT))
        self._recording_time.setDate(QDate.fromString(album.recording_time, ISO_8601_FORMAT))

        self._build_artists_table(album.guest_performers or [])

        identities = album.isnis or {}
        self._main_artist_isni.setText(identities[album.lead_performer] if album.lead_performer in identities else None)

    @staticmethod
    def _display_region(region, combobox):
        combobox.setCurrentText(COUNTRIES[region[0]]) if region else combobox.setCurrentIndex(0)

    def _display_main_artist(self, album):
        # todo this should be set in the embedded metadata adapter and we should have a checkbox for various artists
        self._main_artist.setText(album.compilation and self.tr("Various Artists") or album.lead_performer)
        self._main_artist.setDisabled(album.compilation is True)

    def _metadata(self, *keys):
        all_values = dict(release_name=self._release_name.text(),
                          compilation=self._compilation.isChecked(),
                          lead_performer=self._main_artist.text(),
                          lead_performer_region=self._get_country_code_from_combo(self._main_artist_region),
                          guest_performers=formatting.fromPeopleList(self._artists.text()),
                          label_name=self._label_name.text(),
                          catalog_number=self._catalog_number.text(),
                          upc=self._barcode.text(),
                          comments=self._comments.toPlainText(),
                          recording_time=self._recording_time.date().toString(ISO_8601_FORMAT),
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

    def _disable_mac_focus_frame(self):
        for child in self.findChildren(QWidget):
            child.setAttribute(Qt.WA_MacShowFocusRect, False)

    def _update_isni_menu(self):
        def _is_blank(text):
            return not text or text.strip() == ""

        can_lookup_or_assign = not self._compilation.isChecked() and not _is_blank(self._main_artist.text())
        self._main_artist_isni_actions_button.setEnabled(self._isni_lookup and can_lookup_or_assign)
        self._main_artist_isni_assign_action.setEnabled(self._isni_assign and can_lookup_or_assign)

    def _build_artists_table(self, performers):
        self._clear_artists_table()
        for performer in performers:
            self._build_artist_row(performer)

    def _build_artist_row(self, performer=(None, None)):
        index = self._artists_table_container.count()
        instrument, name = performer

        row_layout = QGridLayout()
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setVerticalSpacing(3)
        row_layout.addWidget(QLabel(self.tr("Instrument")), 0, 0)
        row_layout.addWidget(QLabel(self.tr("Musician Name")), 0, 1)
        row_layout.addWidget(_build_line_edit(name, "_artist_{}".format(index)), 1, 0)
        row_layout.addWidget(_build_line_edit(instrument, "_instrument_{}".format(index)), 1, 1)
        row_layout.addWidget(self._build_remove_line_button(index), 1, 2)
        row_layout.setColumnStretch(0, 1)
        row_layout.setColumnStretch(1, 1)
        row_layout.setColumnStretch(2, 0)
        row_layout.setColumnStretch(3, 1)
        row = QWidget()
        row.setObjectName("_artist_{}".format(index))
        row.setLayout(row_layout)

        self._artists_table_container.addWidget(row)

    def _build_remove_line_button(self, index):
        button = QPushButton()
        button.setObjectName("_remove_artist_{}".format(index))
        button.setCursor(Qt.PointingHandCursor)
        button.setMinimumHeight(22)
        button.setMaximumHeight(22)
        button.setText(self.tr("Remove"))
        button.clicked.connect(lambda: self._remove_artist_row(button.parent()))
        return button

    def _remove_artist_row(self, widget):
        def is_widget_to_remove(index):
            return self._artists_table_container.itemAt(index).widget().objectName() == widget.objectName()

        for current_index in range(self._artists_table_container.count()):
            if is_widget_to_remove(current_index):
                widget = self._artists_table_container.takeAt(current_index).widget()
                widget.setParent(None)
                widget.close()
                break

    def _clear_artists_table(self):
        layout_item = self._artists_table_container.takeAt(0)
        while layout_item:
            widget = layout_item.widget()
            widget.setParent(None)
            widget.close()
            layout_item = self._artists_table_container.takeAt(0)


def _build_line_edit(content, name):
    edit = QLineEdit(content)
    edit.setMinimumWidth(200)
    edit.setObjectName(name)
    edit.setAttribute(Qt.WA_MacShowFocusRect, False)
    return edit
