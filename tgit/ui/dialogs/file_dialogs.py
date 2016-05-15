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

from PyQt5.QtWidgets import QFileDialog


def name_filter(mime_types, name):
    return "{} ({})".format(name, " ".join(["*.{}".format(extension) for extension in mime_types]))


def make_artwork_selection_dialog(artwork_selection, on_file_selected, parent=None, native=True):
    dialog = make_file_dialog(name_filter(artwork_selection.extensions, "Image Files"),
                              QFileDialog.ExistingFile, artwork_selection.directory, parent, native)

    dialog.directoryEntered.connect(artwork_selection.directory_changed)
    dialog.fileSelected.connect(on_file_selected)
    return dialog


def make_export_location_selection_dialog(export_location_selection, on_file_selected, parent=None, native=True):
    dialog = make_save_file_dialog(name_filter(export_location_selection.extensions, "XML File"),
                                   QFileDialog.AnyFile, export_location_selection.directory,
                                   export_location_selection.default_file_name, parent, native)

    dialog.directoryEntered.connect(export_location_selection.directory_changed)
    dialog.fileSelected.connect(on_file_selected)
    return dialog


def make_save_file_dialog(name_filters, file_mode, directory, default_file_name, parent, native):
    dialog = make_file_dialog(name_filters, file_mode, directory, parent, native)
    dialog.selectFile(default_file_name)
    dialog.setAcceptMode(QFileDialog.AcceptSave)
    return dialog


def make_file_dialog(name_filters, file_mode, directory, parent, native):
    dialog = QFileDialog(parent)
    dialog.setOption(QFileDialog.DontUseNativeDialog, not native)
    dialog.setDirectory(directory)
    dialog.setFileMode(file_mode)
    dialog.setNameFilter(dialog.tr(name_filters))
    return dialog
