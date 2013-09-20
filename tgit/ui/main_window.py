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

import mimetypes
from PyQt4.Qt import (Qt, QDir, QRect, QMainWindow, QStatusBar, QWidget, QGridLayout, QPixmap,
                      QImage, QPushButton, QMenu, QMenuBar, QAction, QLabel, QLineEdit,
                      QFileDialog)

from tgit.mp3 import MP3File

MAIN_WINDOW_NAME = "TGiT"
ADD_FILE_BUTTON_NAME = "Add File"
IMPORT_TRACK_DIALOG_NAME = "Select Track File"
SELECT_PICTURE_BUTTON_NAME = "Select Picture"
SELECT_PICTURE_DIALOG_NAME = "Select Picture File"
FRONT_COVER_PICTURE_FILE_NAME = "Front Cover Picture File"
FRONT_COVER_EMBEDDED_TEXT_NAME = "Front Cover Embedded Text"
RELEASE_NAME_NAME = "Release Name"
LEAD_PERFORMER_NAME = "Lead Performer"
ORIGINAL_RELEASE_DATE_NAME = "Original Release Date"
UPC_NAME = "UPC"
TRACK_TITLE_NAME = "Track Title"
VERSION_INFO_NAME = "Version Info"
FEATURED_GUEST_NAME = "Featured Guest"
ISRC_NAME = "ISRC"
BITRATE_NAME = "Bitrate"
DURATION_NAME = "Duration"
SAVE_BUTTON_NAME = "Save"


# todo start teasing apart the main window to get birth to the domain concepts
class MainWindow(QMainWindow):
    def __init__(self, ):
        QMainWindow.__init__(self)
        self._setup_ui()

    def _setup_ui(self):
        self.setObjectName(MAIN_WINDOW_NAME)
        self.resize(640, 480)
        self._make_import_file_dialog()
        self._make_select_picture_dialog()
        self.setCentralWidget(self._make_welcome_panel())
        self._make_tag_album_panel()
        self._fill_menu()
        self._make_status_bar()
        self.localize_ui()

    def _make_status_bar(self):
        self.setStatusBar(QStatusBar(self))

    def _make_welcome_panel(self):
        self._welcome_panel = QWidget()
        welcome_panel_layout = QGridLayout(self._welcome_panel)
        self._add_file_button = QPushButton(self._welcome_panel)
        self._add_file_button.setObjectName(ADD_FILE_BUTTON_NAME)
        self._add_file_button.clicked.connect(self._add_file_dialog.open)
        welcome_panel_layout.addWidget(self._add_file_button, 0, 0, 1, 1)
        return self._welcome_panel

    def _make_tag_album_panel(self):
        self._tag_album_panel = QWidget()
        tag_album_layout = QGridLayout(self._tag_album_panel)
        self._add_front_cover_picture(tag_album_layout, 0)
        self._add_release_name(tag_album_layout, 2)
        self._add_lead_performer(tag_album_layout, 3)
        self._add_original_release_date(tag_album_layout, 4)
        self._add_upc(tag_album_layout, 5)
        self._add_track_title(tag_album_layout, 6)
        self._add_version_info(tag_album_layout, 7)
        self._add_featured_guest(tag_album_layout, 8)
        self._add_isrc(tag_album_layout, 9)
        self._add_bitrate(tag_album_layout, 10)
        self._add_duration(tag_album_layout, 11)
        self._add_buttons(tag_album_layout, 12)
        return self._tag_album_panel

    def _add_front_cover_picture(self, layout, row):
        self._front_cover_image = QLabel(self._tag_album_panel)
        layout.addWidget(self._front_cover_image, row, 0, 1, 1)
        self._select_picture_button = QPushButton(self._tag_album_panel)
        self._select_picture_button.setObjectName(SELECT_PICTURE_BUTTON_NAME)
        self._select_picture_button.clicked.connect(self._select_picture_dialog.open)
        layout.addWidget(self._select_picture_button, row, 1, 1, 1)
        self._front_cover_embedded_text = QLabel(self._tag_album_panel)
        self._front_cover_embedded_text.setObjectName(
            FRONT_COVER_EMBEDDED_TEXT_NAME)
        layout.addWidget(self._front_cover_embedded_text, row + 1, 0, 1, 1)

    def _add_release_name(self, layout, row):
        self._release_name_label = QLabel(self._tag_album_panel)
        layout.addWidget(self._release_name_label, row, 0, 1, 1)
        self._release_name = QLineEdit(self._tag_album_panel)
        self._release_name.setObjectName(RELEASE_NAME_NAME)
        layout.addWidget(self._release_name, row, 1, 1, 1)

    def _add_lead_performer(self, layout, row):
        self._lead_performer_label = QLabel(self._tag_album_panel)
        layout.addWidget(self._lead_performer_label, row, 0, 1, 1)
        self._lead_performer = QLineEdit(self._tag_album_panel)
        self._lead_performer.setObjectName(LEAD_PERFORMER_NAME)
        layout.addWidget(self._lead_performer, row, 1, 1, 1)

    def _add_original_release_date(self, layout, row):
        self._original_release_date_label = QLabel(self._tag_album_panel)
        layout.addWidget(self._original_release_date_label, row, 0, 1, 1)
        self._original_release_date = QLineEdit(self._tag_album_panel)
        self._original_release_date.setObjectName(ORIGINAL_RELEASE_DATE_NAME)
        layout.addWidget(self._original_release_date, row, 1, 1, 1)

    def _add_upc(self, layout, row):
        self._upc_label = QLabel(self._tag_album_panel)
        layout.addWidget(self._upc_label, row, 0, 1, 1)
        self._upc = QLineEdit(self._tag_album_panel)
        self._upc.setObjectName(UPC_NAME)
        layout.addWidget(self._upc, row, 1, 1, 1)

    def _add_track_title(self, layout, row):
        self._track_title_label = QLabel(self._tag_album_panel)
        layout.addWidget(self._track_title_label, row, 0, 1, 1)
        self._track_title = QLineEdit(self._tag_album_panel)
        self._track_title.setObjectName(TRACK_TITLE_NAME)
        layout.addWidget(self._track_title, row, 1, 1, 1)

    def _add_version_info(self, layout, row):
        self._version_info_label = QLabel(self._tag_album_panel)
        layout.addWidget(self._version_info_label, row, 0, 1, 1)
        self._version_info = QLineEdit(self._tag_album_panel)
        self._version_info.setObjectName(VERSION_INFO_NAME)
        layout.addWidget(self._version_info, row, 1, 1, 1)

    def _add_featured_guest(self, layout, row):
        self._featured_guest_label = QLabel(self._tag_album_panel)
        layout.addWidget(self._featured_guest_label, row, 0, 1, 1)
        self._featured_guest = QLineEdit(self._tag_album_panel)
        self._featured_guest.setObjectName(FEATURED_GUEST_NAME)
        layout.addWidget(self._featured_guest, row, 1, 1, 1)

    def _add_isrc(self, layout, row):
        self._isrc_label = QLabel(self._tag_album_panel)
        layout.addWidget(self._isrc_label, row, 0, 1, 1)
        self._isrc = QLineEdit(self._tag_album_panel)
        self._isrc.setObjectName(ISRC_NAME)
        layout.addWidget(self._isrc, row, 1, 1, 1)

    def _add_bitrate(self, layout, row):
        self._bitrate_label = QLabel(self._tag_album_panel)
        layout.addWidget(self._bitrate_label, row, 0, 1, 1)
        self._bitrate = QLabel(self._tag_album_panel)
        self._bitrate.setObjectName(BITRATE_NAME)
        layout.addWidget(self._bitrate, row, 1, 1, 1)

    def _add_duration(self, layout, row):
        self._duration_label = QLabel(self._tag_album_panel)
        layout.addWidget(self._duration_label, row, 0, 1, 1)
        self._duration = QLabel(self._tag_album_panel)
        self._duration.setObjectName(DURATION_NAME)
        layout.addWidget(self._duration, row, 1, 1, 1)

    def _add_buttons(self, layout, row):
        self._save_button = QPushButton(self._tag_album_panel)
        self._save_button.setObjectName(SAVE_BUTTON_NAME)
        self._save_button.clicked.connect(self._save_file)
        layout.addWidget(self._save_button, row, 0, 1, 1)

    def _fill_menu(self):
        menu_bar = QMenuBar(self)
        menu_bar.setGeometry(QRect(0, 0, 469, 21))
        self._quit_menu = QMenu(menu_bar)
        self._quit_menu_item = QAction(self)
        self._quit_menu_item.triggered.connect(self.close)
        self._quit_menu.addAction(self._quit_menu_item)
        self.setMenuBar(menu_bar)
        menu_bar.addAction(self._quit_menu.menuAction())

    # todo integration test dialog file name filtering by making sure the Accept button stay
    # disabled when we select a non supported file type
    def _make_import_file_dialog(self):
        self._add_file_dialog = QFileDialog(self)
        self._add_file_dialog.setObjectName(IMPORT_TRACK_DIALOG_NAME)
        self._add_file_dialog.setDirectory(QDir.homePath())
#        self._add_file_dialog.setOption(QFileDialog.DontUseNativeDialog)
#        self._add_file_dialog.setModal(True)
        self._add_file_dialog.fileSelected.connect(self._import_track_file)

    # todo integration test dialog file name filtering by making sure the Accept button stay
    # disabled when we select a non supported file type
    def _make_select_picture_dialog(self):
        self._select_picture_dialog = QFileDialog(self)
        self._select_picture_dialog.setObjectName(SELECT_PICTURE_DIALOG_NAME)
        self._select_picture_dialog.setDirectory(QDir.homePath())
#        self._select_picture_dialog.setOption(QFileDialog.DontUseNativeDialog)
#        self._select_picture_dialog.setModal(True)
        self._select_picture_dialog.fileSelected.connect(self._load_front_cover_picture)

    def _load_front_cover_picture(self, filename):
        self._display_front_cover(self._load_picture(filename))

    def _display_front_cover(self, picture):
        self._front_cover = picture
        _, image_data = picture
        self._front_cover_image.setPixmap(self._scaled_pixmap_from(image_data))
        self._front_cover_embedded_text.setText(self._embedded_text(image_data))

    def _show_tag_album_panel(self):
        self.setCentralWidget(self._tag_album_panel)

    def _import_track_file(self, filename):
        self._audio = MP3File(filename)
        self._release_name.setText(self._audio.release_name)
        self._display_front_cover(self._audio.front_cover_picture)
        self._lead_performer.setText(self._audio.lead_performer)
        self._original_release_date.setText(self._audio.original_release_date)
        self._upc.setText(self._audio.upc)
        self._track_title.setText(self._audio.track_title)
        self._version_info.setText(self._audio.version_info)
        self._featured_guest.setText(self._audio.featured_guest)
        self._isrc.setText(self._audio.isrc)
        self._bitrate.setText("%d kbps" % self._audio.bitrate_in_kbps)
        self._duration.setText(self._audio.duration_as_text)
        self._show_tag_album_panel()

    def _embedded_text(self, image_data):
            return QImage.fromData(image_data).text()

    def _scaled_pixmap_from(self, image_data):
        if image_data is None:
            return QPixmap()
        original_image = QImage.fromData(image_data)
        scaled_image = original_image.scaled(125, 125, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return QPixmap.fromImage(scaled_image)

    def _save_file(self):
        self._audio.release_name = self._release_name.text()
        self._audio.front_cover_picture = self._front_cover
        self._audio.lead_performer = self._lead_performer.text()
        self._audio.original_release_date = self._original_release_date.text()
        self._audio.upc = self._upc.text()
        self._audio.track_title = self._track_title.text()
        self._audio.version_info = self._version_info.text()
        self._audio.featured_guest = self._featured_guest.text()
        self._audio.isrc = self._isrc.text()
        self._audio.save()

    def _load_picture(self, filename):
        if filename is None:
            return None, None
        mime_type = mimetypes.guess_type(filename)
        image_data = open(filename, "rb").read()
        return mime_type[0], image_data

    def localize_ui(self):
        self.setWindowTitle(self.tr("TGiT"))
        self._add_file_button.setText(self.tr("Add File..."))
        self._quit_menu.setTitle(self.tr("Quit"))
        self._quit_menu_item.setText(self.tr("Hit me to quit"))
        self._release_name_label.setText(self.tr("Release Name: "))
        self._lead_performer_label.setText(self.tr("Lead Performer: "))
        self._original_release_date_label.setText(self.tr("Original Release Date: "))
        self._upc_label.setText(self.tr("UPC/EAN: "))
        self._track_title_label.setText(self.tr("Track Title: "))
        self._version_info_label.setText(self.tr("Version Information: "))
        self._featured_guest_label.setText(self.tr("Featured Guest: "))
        self._isrc_label.setText(self.tr("ISRC: "))
        self._bitrate_label.setText(self.tr("Bitrate: "))
        self._duration_label.setText(self.tr("Duration: "))
        self._save_button.setText(self.tr("Save"))
        self._add_file_dialog.setNameFilter(self.tr("MP3 files") + " (*.mp3)")
        self._select_picture_button.setText(self.tr("Select Picture..."))
        self._select_picture_dialog.setNameFilter(self.tr("Image files") + " (*.png)")