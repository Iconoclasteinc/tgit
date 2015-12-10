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

from PyQt5.QtCore import Qt, pyqtSignal, QDate
from PyQt5.QtWidgets import QWidget, QApplication, QMenu
import requests

from tgit.album import AlbumListener
from tgit.auth import Permission
from tgit.authentication_error import AuthenticationError
from tgit.countries import COUNTRIES
from tgit.insufficient_information_error import InsufficientInformationError
from tgit.signal import MultiSubscription
from tgit.ui.closeable import Closeable
from tgit.ui.helpers.ui_file import UIFile
from tgit.ui.helpers import image, formatting

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
                            show_cheddar_authentication_failed, **handlers):
    page = AlbumEditionPage(select_picture=select_picture,
                            edit_performers=edit_performers,
                            select_identity=select_identity,
                            review_assignation=review_assignation,
                            show_isni_assignation_failed=show_isni_assignation_failed,
                            show_cheddar_connection_failed=show_cheddar_connection_failed,
                            show_cheddar_authentication_failed=show_cheddar_authentication_failed)
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

    FRONT_COVER_SIZE = 350, 350

    def __init__(self, edit_performers, select_picture, select_identity, review_assignation,
                 show_isni_assignation_failed, show_cheddar_connection_failed, show_cheddar_authentication_failed):
        super().__init__()
        self._show_cheddar_authentication_failed = show_cheddar_authentication_failed
        self._review_assignation = review_assignation
        self._show_cheddar_connection_failed = show_cheddar_connection_failed
        self._show_isni_assignation_failed = show_isni_assignation_failed
        self._select_identity = select_identity
        self._select_picture = select_picture
        self._edit_performers = edit_performers
        self._setup_ui()

    def _setup_ui(self):
        self._load(":/ui/album_page.ui")
        self._disable_mac_focus_frame()

        self._fill_with_countries(self._lead_performer_region)

        menu = QMenu()
        menu.setStyleSheet(QMENU_STYLESHEET)
        menu.addAction(self._main_artist_isni_lookup_action)
        menu.addAction(self._main_artist_isni_assign_action)
        self._isni_actions_button.setMenu(menu)

        self.compilation.clicked.connect(self._update_isni_lookup_button)
        self.lead_performer.textChanged.connect(self._update_isni_lookup_button)
        self.add_guest_performers_button.clicked.connect(lambda: self._edit_performers(self._update_guest_performers))

    @staticmethod
    def _fill_with_countries(combobox):
        for code, name in sorted(COUNTRIES.items(), key=operator.itemgetter(1)):
            combobox.addItem(name, code)
        combobox.insertItem(0, "")
        combobox.setCurrentIndex(0)

    def on_select_picture(self, on_select_picture):
        self.select_picture_button.clicked.connect(lambda: self._select_picture(on_select_picture))

    def on_isni_lookup(self, on_isni_lookup):
        def start_waiting():
            QApplication.setOverrideCursor(Qt.WaitCursor)
            try:
                on_isni_lookup(self.lead_performer.text(), on_lookup_success)
            except requests.ConnectionError:
                self._show_cheddar_connection_failed()
            except AuthenticationError:
                self._show_cheddar_authentication_failed()
            finally:
                QApplication.restoreOverrideCursor()

        def on_lookup_success(identities):
            self._select_identity(identities)
            QApplication.restoreOverrideCursor()

        self._main_artist_isni_lookup_action.triggered.connect(start_waiting)

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
            self._isni.setFocus(Qt.OtherFocusReason)
            self._isni.setText(identity.id)
            QApplication.restoreOverrideCursor()

        self._main_artist_isni_assign_action.triggered.connect(lambda _: self._review_assignation(start_waiting))

    def on_remove_picture(self, on_remove_picture):
        self.remove_picture_button.clicked.connect(lambda _: on_remove_picture())

    def on_metadata_changed(self, handler):
        def handle(entry):
            handler(**self.metadata(entry))

        self.release_time.dateChanged.connect(lambda: handle("release_time"))
        self.digital_release_time.dateChanged.connect(lambda: handle("digital_release_time"))
        self.original_release_time.dateChanged.connect(lambda: handle("original_release_time"))
        self.recording_time.dateChanged.connect(lambda: handle("recording_time"))
        self.release_name.editingFinished.connect(lambda: handle("release_name"))
        self.compilation.clicked.connect(lambda: handle("compilation"))
        self.lead_performer.editingFinished.connect(lambda: handle("lead_performer"))
        self._lead_performer_region.activated.connect(lambda: handle("lead_performer_region"))
        self._isni.editingFinished.connect(lambda: handle("isni"))
        self.guest_performers.textChanged.connect(lambda: handle("guest_performers"))
        self.label_name.editingFinished.connect(lambda: handle("label_name"))
        self.catalog_number.editingFinished.connect(lambda: handle("catalog_number"))
        self.barcode.editingFinished.connect(lambda: handle("upc"))
        self.media_type.editingFinished.connect(lambda: handle("media_type"))
        self.release_type.editingFinished.connect(lambda: handle("release_type"))
        self.comments.editingFinished.connect(lambda: handle("comments"))

    def _update_guest_performers(self, performers):
        self.guest_performers.setText(formatting.toPeopleList(performers))

    def albumStateChanged(self, album):
        self.display(album)

    def user_changed(self, user):
        self._isni_lookup = user.has_permission(Permission.isni_lookup)
        if not self._isni_lookup:
            self._main_artist_isni_lookup_action.setToolTip(self.tr("Please sign-in to activate ISNI lookup"))
        else:
            self._main_artist_isni_lookup_action.setToolTip(None)
        self._update_isni_lookup_button()

    def display(self, album):
        if album.main_cover is not self._picture or album.main_cover is None:
            self.front_cover.setPixmap(image.scale(album.main_cover, *self.FRONT_COVER_SIZE))
            self._picture = album.main_cover
        self.release_name.setText(album.release_name)
        self.compilation.setChecked(album.compilation is True)
        self._display_lead_performer(album)
        self._display_region(album.lead_performer_region, self._lead_performer_region)
        self._isni.setText(album.lead_performer[1] if album.lead_performer and len(album.lead_performer) > 1 else "")
        self.guest_performers.setText(formatting.toPeopleList(album.guest_performers))
        self.label_name.setText(album.label_name)
        self.catalog_number.setText(album.catalog_number)
        self.barcode.setText(album.upc)
        self.comments.setPlainText(album.comments)
        self.release_time.setDate(QDate.fromString(album.release_time, ISO_8601_FORMAT))
        self.recording_time.setDate(QDate.fromString(album.recording_time, ISO_8601_FORMAT))

    @staticmethod
    def _display_region(region, combobox):
        combobox.setCurrentText(COUNTRIES[region[0]]) if region else combobox.setCurrentIndex(0)

    def _display_lead_performer(self, album):
        # todo this should be set in the embedded metadata adapter and we should have a checkbox for various artists
        self.lead_performer.setText(
            album.compilation and self.tr("Various Artists") or album.lead_performer[0] if album.lead_performer else "")
        self.lead_performer.setDisabled(album.compilation is True)

    def metadata(self, *keys):
        all_values = dict(release_name=self.release_name.text(),
                          compilation=self.compilation.isChecked(),
                          lead_performer_region=self._get_country_code_from_combo(self._lead_performer_region),
                          guest_performers=formatting.fromPeopleList(self.guest_performers.text()),
                          label_name=self.label_name.text(),
                          catalog_number=self.catalog_number.text(),
                          upc=self.barcode.text(),
                          comments=self.comments.toPlainText(),
                          recording_time=self.recording_time.date().toString(ISO_8601_FORMAT),
                          release_time=self.release_time.date().toString(ISO_8601_FORMAT))

        if self._isni.text():
            all_values["lead_performer"] = (self.lead_performer.text(), self._isni.text())
        else:
            all_values["lead_performer"] = (self.lead_performer.text(),)

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

    def _update_isni_lookup_button(self):
        def _is_blank(text):
            return not text or text.strip() == ""

        self._main_artist_isni_lookup_action.setEnabled(
            self._isni_lookup and not self.compilation.isChecked() and not _is_blank(self.lead_performer.text()))
