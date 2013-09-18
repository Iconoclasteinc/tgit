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
FRONT_COVER_PICTURE_FILE_NAME = "Front Cover Picture File"
FRONT_COVER_EMBEDDED_TEXT_NAME = "Front Cover Embedded Text"
RELEASE_NAME_NAME = "Release Name"
LEAD_PERFORMER_NAME = "Lead Performer"
TRACK_TITLE_NAME = "Track Title"
VERSION_INFO_NAME = "Version Info"
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
        self._add_file_button.clicked.connect(self._add_file_dialog.show)
        welcome_panel_layout.addWidget(self._add_file_button, 0, 0, 1, 1)
        return self._welcome_panel

    def _make_tag_album_panel(self):
        self._tag_album_panel = QWidget()
        tag_album_layout = QGridLayout(self._tag_album_panel)
        self._add_front_cover_picture(tag_album_layout, 0)
        self._add_release_name(tag_album_layout, 2)
        self._add_lead_performer(tag_album_layout, 3)
        self._add_track_title(tag_album_layout, 4)
        self._add_version_info(tag_album_layout, 5)
        self._add_bitrate(tag_album_layout, 6)
        self._add_duration(tag_album_layout, 7)
        self._add_buttons(tag_album_layout, 8)
        return self._tag_album_panel

    def _add_front_cover_picture(self, layout, row):
        self._front_cover_image = QLabel(self._tag_album_panel)
        layout.addWidget(self._front_cover_image, row, 0, 1, 1)
        self._front_cover_file = QLineEdit(self._tag_album_panel)
        self._front_cover_file.setObjectName(
            FRONT_COVER_PICTURE_FILE_NAME)
        layout.addWidget(self._front_cover_file, row, 1, 1, 1)
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
        self._add_file_dialog.setDirectory(QDir.homePath())
        self._add_file_dialog.setOption(QFileDialog.DontUseNativeDialog)
        self._add_file_dialog.setModal(True)
        self._add_file_dialog.fileSelected.connect(self._import_file)

    def _show_tag_album_panel(self):
        self.setCentralWidget(self._tag_album_panel)

    def _import_file(self, filename):
        self.audio = MP3File(filename)
        self._release_name.setText(self.audio.release_name)
        self._front_cover_image.setPixmap(self._scaled_pixmap_from(self.audio.front_cover_picture))
        self._front_cover_embedded_text.setText(self._embedded_text(self.audio.front_cover_picture))
        self._lead_performer.setText(self.audio.lead_performer)
        self._track_title.setText(self.audio.track_title)
        self._bitrate.setText("%d kps" % self.audio.bitrate_in_kbps)
        self._duration.setText(self.audio.duration_as_text)
        self._show_tag_album_panel()

    def _embedded_text(self, image_data):
        return QImage.fromData(image_data).text()

    def _scaled_pixmap_from(self, image_data):
        original_image = QImage.fromData(image_data)
        scaled_image = original_image.scaled(125, 125, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return QPixmap.fromImage(scaled_image)

    def _save_file(self):
        self.audio.release_name = self._release_name.text()
        self.audio.front_cover_picture = self._load_picture(self._front_cover_file.text())
        self.audio.lead_performer = self._lead_performer.text()
        self.audio.track_title = self._track_title.text()
        self.audio.version_info = self._version_info.text()
        self.audio.save()

    def _load_picture(self, filename):
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
        self._track_title_label.setText(self.tr("Track Title: "))
        self._version_info_label.setText(self.tr("Version Information: "))
        self._bitrate_label.setText(self.tr("Bitrate: "))
        self._duration_label.setText(self.tr("Duration: "))
        self._save_button.setText(self.tr("Save"))
        self._add_file_dialog.setNameFilter(self.tr("MP3 files") + " (*.mp3)")