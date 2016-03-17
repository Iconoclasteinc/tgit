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
import functools

import tgit.identity as identity
from tgit import album_director as director
from tgit.ui.dialogs.isni_lookup_dialog import make_isni_lookup_dialog
from tgit.ui.pages.new_project_page import make_new_project_page
from tgit.ui.pages.project_edition_page import make_project_edition_page
from tgit.ui.pages.project_screen import make_project_screen
from tgit.ui.pages.startup_screen import StartupScreen
from tgit.ui.pages.track_edition_page import make_track_edition_page
from tgit.ui.pages.track_list_tab import make_track_list_tab
from tgit.ui.pages.welcome_page import make_welcome_page


class Pages:
    def __init__(self, dialogs, messages, session, portfolio, player, cheddar, identity_lookup):
        self._identity_lookup = identity_lookup
        self._cheddar = cheddar
        self._player = player
        self._session = session
        self._messages = messages
        self._dialogs = dialogs
        self._portfolio = portfolio

    def startup_screen(self):
        return StartupScreen(create_welcome_page=self._welcome_page,
                             create_new_project_page=self._new_project_page)

    def project_screen(self, album):
        return make_project_screen(album=album,
                                   project_page=self._project_edition_page,
                                   track_page=self._track_page_for(album))

    def _new_project_page(self):
        return make_new_project_page(select_location=self._dialogs.select_project_destination,
                                     select_track=self._dialogs.select_track,
                                     check_project_exists=director.album_exists,
                                     confirm_overwrite=self._messages.overwrite_project_confirmation,
                                     on_create_project=director.create_album_into(self._portfolio))

    def _welcome_page(self):
        return make_welcome_page(select_project=self._dialogs.select_project_to_load,
                                 show_load_error=self._messages.load_project_failed,
                                 on_load_project=director.load_album_into(self._portfolio))

    def _track_list_tab(self, album):
        return make_track_list_tab(album=album, player=self._player,
                                   select_tracks=functools.partial(self._dialogs.select_tracks, album.type),
                                   on_move_track=director.move_track_of(album),
                                   on_remove_track=director.remove_track_from(album),
                                   on_play_track=self._player.play,
                                   on_stop_track=self._player.stop,
                                   on_add_tracks=director.add_tracks_to(album))

    def _project_edition_page(self, album):
        return make_project_edition_page(
            album=album,
            session=self._session,
            identity_lookup=self._identity_lookup,
            track_list_tab=self._track_list_tab,
            review_assignation=self._dialogs.review_isni_assignation_in(album, True),
            show_isni_assignation_failed=self._messages.isni_assignation_failed,
            show_cheddar_connection_failed=self._messages.cheddar_connection_failed,
            show_cheddar_authentication_failed=self._messages.cheddar_authentication_failed,
            show_permission_denied=self._messages.permission_denied,
            select_picture=self._dialogs.select_cover,
            on_select_picture=director.change_cover_of(album),
            on_isni_changed=director.add_isni_to(album),
            on_isni_local_lookup=director.lookup_isni_in(album),
            on_identity_selection=self._isni_dialog,
            on_isni_assign=director.assign_isni_to_main_artist_using(self._cheddar, self._session, album),
            on_remove_picture=director.remove_album_cover_from(album),
            on_metadata_changed=director.update_album_from(album))

    def _track_page_for(self, album):
        def track_page(track):
            return make_track_edition_page(
                album=album,
                track=track,
                on_track_changed=director.update_track(track),
                on_isni_local_lookup=director.lookup_isni_in(album),
                on_ipi_local_lookup=director.lookup_ipi_in(album),
                on_ipi_changed=director.add_ipi_to(album),
                review_assignation=self._dialogs.review_isni_assignation_in(album),
                show_isni_assignation_failed=self._messages.isni_assignation_failed,
                show_cheddar_connection_failed=self._messages.cheddar_connection_failed,
                show_cheddar_authentication_failed=self._messages.cheddar_authentication_failed)

        return track_page

    def _isni_dialog(self, parent, query):
        return make_isni_lookup_dialog(parent,
                                       self._identity_lookup,
                                       on_lookup=identity.launch_lookup(self._cheddar, self._session,
                                                                        self._identity_lookup)).lookup(query)
