# -*- coding: utf-8 -*-
# todo remove this import
from ._screen_driver import ScreenDriver

from .export_as_dialog_driver import export_as_dialog
from .picture_selection_dialog_driver import picture_selection_dialog, PictureSelectionDialogDriver
from .track_selection_dialog_driver import track_selection_dialog, TrackSelectionDialogDriver
from .import_album_from_track_dialog_driver import import_album_from_track_dialog, ImportAlbumFromTrackDialogDriver

from .album_composition_page_driver import album_composition_page, AlbumCompositionPageDriver
from .album_edition_page_driver import album_edition_page, AlbumEditionPageDriver
from .album_screen_driver import album_screen, AlbumScreenDriver
from .menu_bar_driver import menu_bar, MenuBarDriver
from .performer_dialog_driver import PerformerDialogDriver
from .settings_dialog_driver import settings_dialog, SettingsDialogDriver
from .track_edition_page_driver import track_edition_page, TrackEditionPageDriver

from .welcome_screen_driver import welcome_screen, WelcomeScreenDriver
