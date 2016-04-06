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
from .loader import Loader

from .ui_about_dialog import Ui_about_tgit_dialog as AboutTgitDialog
from .ui_isni_assignation_review_dialog import Ui_isni_assignation_review_dialog as ISNIAssignationReviewDialog
from .ui_isni_dialog import Ui_isni_lookup_dialog as ISNIDialog
from .ui_main_window import Ui_main_window as MainWindow
from .ui_musician_row import Ui__musician_row as MusicianRow
from .ui_musician_tab import Ui__musician_table_widget as MusicianTab
from .ui_new_project_page import Ui_new_project_page as NewProjectPage
from .ui_project_page import Ui_project_edition_page as ProjectEditionPage
from .ui_project_screen import Ui_project_screen as ProjectScreen
from .ui_settings_dialog import Ui_settings_dialog as SettingsDialog
from .ui_sign_in_dialog import Ui_sign_in_dialog as SignInDialog
from .ui_track_list_tab import Ui_track_list_tab as TrackListTab
from .ui_track_page import Ui_track_edition_page as TrackEditionPage
from .ui_welcome_page import Ui_welcome_page as WelcomePage

welcome_page = Loader(WelcomePage)
