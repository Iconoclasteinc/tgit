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

from queue import Queue

from PyQt5.QtCore import Qt, pyqtSignal, QDate, QEventLoop
from PyQt5.QtWidgets import QWidget, QLabel, QApplication

from .helpers import image, formatting, ui_file
from tgit import album_director as director
from tgit.album import AlbumListener
from tgit.genres import GENRES
from tgit.isni.name_registry import NameRegistry
from tgit.util import async_task_runner as task_runner


def make_album_edition_page(dialogs, lookup_isni_dialog_factory, activity_indicator_dialog_factory,
                            performer_dialog_factory, show_assignation_failed, album, name_registry,
                            use_local_isni_backend):
    def poll_queue():
        while queue.empty():
            QApplication.processEvents(QEventLoop.AllEvents, 100)
        return queue.get(True)

    def lookup_isni():
        activity_dialog = activity_indicator_dialog_factory()
        activity_dialog.show()
        task_runner.runAsync(lambda: director.lookupISNI(name_registry, album.lead_performer)).andPutResultInto(
            queue).run()

        identities = poll_queue()
        activity_dialog.close()
        dialog = lookup_isni_dialog_factory(album, identities)
        dialog.show()

    def assign_isni():
        activity_dialog = activity_indicator_dialog_factory()
        activity_dialog.show()
        task_runner.runAsync(lambda: director.assign_isni(name_registry, album)).andPutResultInto(queue).run()
        code, payload = poll_queue()
        activity_dialog.close()
        if code == NameRegistry.Codes.SUCCESS:
            album.isni = payload
        else:
            show_assignation_failed(payload)

    def add_performer():
        dialog = performer_dialog_factory(album)
        dialog.show()

    queue = Queue()
    page = AlbumEditionPage(use_local_isni_backend)
    page.metadata_changed.connect(lambda metadata: director.updateAlbum(album, **metadata))
    page.select_picture.connect(lambda: dialogs.select_cover(album).open())
    page.remove_picture.connect(lambda: director.removeAlbumCover(album))
    page.lookup_isni.connect(lookup_isni)
    page.assign_isni.connect(assign_isni)
    page.clear_isni.connect(lambda: director.clearISNI(album))
    page.add_performer.connect(add_performer)
    album.addAlbumListener(page)
    page.refresh(album)
    return page


class AlbumEditionPage(QWidget, AlbumListener):
    select_picture = pyqtSignal()
    remove_picture = pyqtSignal()
    lookup_isni = pyqtSignal()
    clear_isni = pyqtSignal()
    assign_isni = pyqtSignal()
    add_performer = pyqtSignal()
    metadata_changed = pyqtSignal(dict)

    FRONT_COVER_SIZE = 350, 350

    def __init__(self, use_local_isni_backend=False):
        super().__init__()
        ui_file.load(":/ui/album_page.ui", self)
        self.use_local_isni_backend = use_local_isni_backend
        self.picture = None

        self._disable_mac_focus_frame()

        # picture box
        self.front_cover.setFixedSize(*self.FRONT_COVER_SIZE)
        self.select_picture_button.clicked.connect(lambda pressed: self.select_picture.emit())
        self.remove_picture_button.clicked.connect(lambda pressed: self.remove_picture.emit())

        # date box
        self.release_time.dateChanged.connect(lambda: self.metadata_changed.emit(self.metadata("releaseTime")))
        self.digital_release_time.dateChanged.connect(
            lambda: self.metadata_changed.emit(self.metadata("digitalReleaseTime")))
        self.original_release_time.dateChanged.connect(
            lambda: self.metadata_changed.emit(self.metadata("originalReleaseTime")))
        self.recording_time.dateChanged.connect(lambda: self.metadata_changed.emit(self.metadata("recording_time")))

        # album box
        self.release_name.editingFinished.connect(lambda: self.metadata_changed.emit(self.metadata("release_name")))
        self.lookup_isni_button.clicked.connect(lambda pressed: self.lookup_isni.emit())
        self.assign_isni_button.clicked.connect(lambda: self.assign_isni.emit())
        self.compilation.clicked.connect(lambda: self.metadata_changed.emit(self.metadata("compilation")))
        self.compilation.clicked.connect(self._adjust_isni_lookup_state_on_compilation_changed)
        self.lead_performer.editingFinished.connect(lambda: self.metadata_changed.emit(self.metadata("lead_performer")))
        self.lead_performer.textChanged.connect(self._adjust_isni_lookup_and_assign_state_on_lead_performer_changed)
        self.clear_isni_button.clicked.connect(lambda: self.clear_isni.emit())
        self.clear_isni_button.clicked.connect(lambda: self.release_time.calendarWidget().show())
        self.add_guest_performers_button.clicked.connect(lambda: self.add_performer.emit())
        self.guest_performers.editingFinished.connect(
            lambda: self.metadata_changed.emit(self.metadata("guestPerformers")))

        # record
        self.label_name.editingFinished.connect(lambda: self.metadata_changed.emit(self.metadata("label_name")))
        self.catalog_number.editingFinished.connect(lambda: self.metadata_changed.emit(self.metadata("catalogNumber")))
        self.barcode.editingFinished.connect(lambda: self.metadata_changed.emit(self.metadata("upc")))
        self.media_type.editingFinished.connect(lambda: self.metadata_changed.emit(self.metadata("media_type")))
        self.release_type.editingFinished.connect(lambda: self.metadata_changed.emit(self.metadata("releaseType")))
        self.comments.editingFinished.connect(lambda: self.metadata_changed.emit(self.metadata("comments")))

        # recording
        self.recording_studios.editingFinished.connect(
            lambda: self.metadata_changed.emit(self.metadata("recordingStudios")))
        self.producer.editingFinished.connect(lambda: self.metadata_changed.emit(self.metadata("producer")))
        self.mixer.editingFinished.connect(lambda: self.metadata_changed.emit(self.metadata("mixer")))
        self.genre.addItems(sorted(GENRES))
        self.genre.activated.connect(lambda: self.metadata_changed.emit(self.metadata("primary_style")))
        self.genre.lineEdit().textEdited.connect(
            lambda: self.metadata_changed.emit(self.metadata("primary_style")))

    def albumStateChanged(self, album):
        self.refresh(album)

    def refresh(self, album):
        if album.mainCover is not self.picture or album.mainCover is None:
            self.front_cover.setPixmap(image.scale(album.mainCover, *self.FRONT_COVER_SIZE))
            self.picture = album.mainCover
        self.release_name.setText(album.release_name)
        self.compilation.setChecked(album.compilation is True)
        self._display_lead_performer(album)
        self.isni.setText(album.isni)
        self.guest_performers.setText(formatting.toPeopleList(album.guestPerformers))
        self.label_name.setText(album.label_name)
        self.catalog_number.setText(album.catalogNumber)
        self.barcode.setText(album.upc)
        self.comments.setPlainText(album.comments)
        self.release_time.setDate(QDate.fromString(album.releaseTime, "yyyy-MM-dd"))
        self.recording_time.setDate(QDate.fromString(album.recording_time, "yyyy-MM-dd"))
        self.recording_studios.setText(album.recordingStudios)
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
                          guestPerformers=formatting.fromPeopleList(self.guest_performers.text()),
                          label_name=self.label_name.text(),
                          catalogNumber=self.catalog_number.text(),
                          upc=self.barcode.text(),
                          comments=self.comments.toPlainText(),
                          recording_time=self.recording_time.date().toString("yyyy-MM-dd"),
                          releaseTime=self.release_time.date().toString("yyyy-MM-dd"),
                          recordingStudios=self.recording_studios.text(),
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

    def _label_for(self, widget):
        def with_buddy(buddy):
            return lambda w: w.buddy() == buddy

        return self._child_widget(QLabel, with_buddy(widget))

    def _child_widget(self, of_type, matching):
        return next(child for child in self.findChildren(of_type) if matching(child))

    def _adjust_isni_lookup_state_on_compilation_changed(self):
        buttons = [self.lookup_isni_button]
        self._enable_or_disable_isni_button(self.compilation.isChecked(), self.lead_performer.text(), buttons)

    def _adjust_isni_lookup_and_assign_state_on_lead_performer_changed(self, text):
        buttons = [self.lookup_isni_button]
        if self.use_local_isni_backend and buttons.count(self.assign_isni_button) == 0:
            buttons.append(self.assign_isni_button)

        self._enable_or_disable_isni_button(self.compilation.isChecked(), text, buttons)

    @staticmethod
    def _enable_or_disable_isni_button(compilation, lead_performer, buttons):
        is_disabled = compilation or is_blank(lead_performer)
        for button in buttons:
            button.setDisabled(is_disabled)


def is_blank(text):
    return not text or text.strip() == ""
