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

from tgit.ui.message_box import close_album_confirmation_box


def import_album_in(portfolio, dialogs):
    def import_album():
        dialogs.import_album(portfolio).open()

    return import_album


def load_album_in(portfolio, dialogs):
    def load_album():
        dialogs.load_album_file(portfolio).open()

    return load_album


def close_album_and(remove_album):
    def close_album(album, window):
        confirmation = close_album_confirmation_box(window)
        confirmation.yes.connect(lambda: remove_album(album))
        confirmation.open()

    return close_album


def add_files_to(dialogs):
    def add_files(album):
        dialogs.add_tracks(album).open()

    return add_files


def add_folder_to(dialogs):
    def add_folder(album):
        dialogs.add_tracks_in_folder(album).open()

    return add_folder


def export_to(dialogs):
    def export(album):
        dialogs.export(album).open()

    return export
