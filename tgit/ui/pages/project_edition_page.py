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
from tgit.auth import Permission
from tgit.countries import COUNTRIES
from tgit.signal import MultiSubscription
from tgit.ui import pixmap
from tgit.ui.closeable import Closeable
from tgit.ui.helpers.ui_file import UIFile

ISO_8601_FORMAT = "yyyy-MM-dd"


def make_project_edition_page(project, session, track_list_tab, on_select_artwork, on_select_identity, on_isni_changed,
                              **handlers):
    track_list = track_list_tab(project)
    page = ProjectEditionPage(track_list_tab=track_list)
    page.on_select_artwork.connect(on_select_artwork)
    page.on_select_identity.connect(on_select_identity)
    page.on_isni_edited.connect(on_isni_changed)

    for name, handler in handlers.items():
        getattr(page, name)(handler)

    subscriptions = MultiSubscription()
    subscriptions += session.user_signed_in.subscribe(page.user_changed)
    subscriptions += session.user_signed_out.subscribe(lambda user: page.user_changed(session.current_user))
    page.closed.connect(lambda: subscriptions.cancel())
    page.closed.connect(track_list.close)

    project.addAlbumListener(page)
    page.closed.connect(lambda: project.removeAlbumListener(page))
    page.user_changed(session.current_user)
    page.display(project)
    return page


@Closeable
class ProjectEditionPage(QWidget, UIFile, AlbumListener):
    closed = pyqtSignal()
    on_select_artwork = pyqtSignal()
    on_select_identity = pyqtSignal(str)
    on_isni_edited = pyqtSignal(str, str)

    _picture = None
    _isni_lookup = False
    _isni_assign = False

    FRONT_COVER_SIZE = 200, 200

    def __init__(self, track_list_tab):
        super().__init__()
        self._setup_ui(track_list_tab)

    def _setup_ui(self, track_list_tab):
        self._load(":/ui/project_page.ui")
        self._fill_with_countries(self._main_artist_region)
        # We can't use class attributes because we need Qt to be initialized
        self._no_cover = pixmap.none(*self.FRONT_COVER_SIZE)
        self._broken_cover = pixmap.broken(*self.FRONT_COVER_SIZE)
        self._front_cover.setPixmap(self._no_cover)
        self._compilation.clicked.connect(self._update_isni_menu)
        self._main_artist.textChanged.connect(self._update_isni_menu)
        self._tabs.widget(0).layout().addWidget(track_list_tab)

        self._main_artist_isni_actions_button.clicked.connect(
            lambda: self.on_select_identity.emit(self._main_artist.text()))

        self._main_artist_isni.editingFinished.connect(
            lambda: self.on_isni_edited.emit(self._main_artist.text(), self._main_artist_isni.text()))

        self._select_artwork_button.clicked.connect(lambda: self.on_select_artwork.emit())

    @staticmethod
    def _fill_with_countries(combobox):
        for code, name in sorted(COUNTRIES.items(), key=operator.itemgetter(1)):
            combobox.addItem(name, code)
        combobox.insertItem(0, "")
        combobox.setCurrentIndex(0)

    def on_isni_local_lookup(self, on_isni_local_lookup):
        def update_main_artist_isni(main_artist):
            self._main_artist_isni.setText(on_isni_local_lookup(main_artist))

        self._main_artist.textEdited.connect(update_main_artist_isni)

    def on_remove_artwork(self, on_remove_artwork):
        self._remove_artwork_button.clicked.connect(lambda: on_remove_artwork())

    def on_metadata_changed(self, handler):
        def handle(entry, musicians=None):
            handler(**self._metadata(musicians, entry))

        self._musician_table_container.on_musician_changed(lambda musicians: handle("guest_performers", musicians))
        self._release_time.dateChanged.connect(lambda: handle("release_time"))
        self._title.editingFinished.connect(lambda: handle("release_name"))
        self._compilation.clicked.connect(lambda: handle("compilation"))
        self._main_artist.editingFinished.connect(lambda: handle("lead_performer"))
        self._main_artist_region.currentIndexChanged.connect(lambda: handle("lead_performer_region"))
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
        self._display_cover(album.main_cover)
        self._title.setText(album.release_name)
        self._display_main_artist(album)
        self._label_name.setText(album.label_name)
        self._catalog_number.setText(album.catalog_number)
        self._barcode.setText(album.upc)
        self._release_time.setDate(QDate.fromString(album.release_time, ISO_8601_FORMAT))
        self._musician_table_container.display(album.guest_performers or [])

    def _display_cover(self, cover):
        if cover is not self._picture:
            self._picture = cover
            self._front_cover.setPixmap(self._scale_cover(cover))

    def _scale_cover(self, cover):
        if not cover:
            return self._no_cover
        scaled_cover = pixmap.from_image(imager.scale(cover, *self.FRONT_COVER_SIZE))
        return self._broken_cover if scaled_cover.isNull() else scaled_cover

    def _display_main_artist(self, album):
        def displayed_main_artist():
            return self.tr("Various Artists") if is_compilation() else album.lead_performer

        def is_compilation():
            return album.compilation is True

        self._compilation.setChecked(is_compilation())
        self._main_artist.setDisabled(is_compilation())
        self._main_artist.setText(displayed_main_artist())
        self._main_artist_caption.setDisabled(is_compilation())
        self._main_artist_isni.setDisabled(is_compilation())
        self._main_artist_isni.setText((album.isnis or {}).get(album.lead_performer))
        self._main_artist_isni_caption.setDisabled(is_compilation())
        self._main_artist_isni_help.setDisabled(is_compilation())
        self._main_artist_region.setDisabled(is_compilation())
        self._main_artist_region_caption.setDisabled(is_compilation())

        if is_compilation() or not album.lead_performer_region:
            self._main_artist_region.setCurrentIndex(0)
        else:
            self._main_artist_region.setCurrentText(COUNTRIES[album.lead_performer_region[0]])

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

        return {k: all_values.get(k, None) for k in keys}

    @staticmethod
    def _get_country_code_from_combo(combo):
        return (combo.currentData(),) if combo.currentIndex() > 0 else None

    def _update_isni_menu(self):
        def _is_blank(text):
            return not text or text.strip() == ""

        can_lookup_or_assign = not self._compilation.isChecked() and not _is_blank(self._main_artist.text())
        self._main_artist_isni_actions_button.setEnabled(self._isni_lookup and can_lookup_or_assign)


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
