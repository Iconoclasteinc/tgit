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

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QEventLoop
from tgit.album import AlbumListener

from tgit.isni.name_registry import NameRegistry
from tgit import album_director as director
from tgit.export.csv_format import CsvFormat
from tgit.ui.activity_indicator_dialog import ActivityIndicatorDialog
from tgit.ui.import_album_from_track_dialog import ImportAlbumFromTrackDialog
from tgit.ui.isni_lookup_dialog import ISNILookupDialog
from tgit.ui.performer_dialog import PerformerDialog
from tgit.ui.album_composition_page import AlbumCompositionPage
from tgit.ui.album_edition_page import AlbumEditionPage
from tgit.ui.export_as_dialog import ExportAsDialog
from tgit.ui.main_window import MainWindow
from tgit.ui.restart_message_box import RestartMessageBox
from tgit.ui.restart_message_box import isni_assignation_failed_message_box
from tgit.ui.picture_selection_dialog import PictureSelectionDialog
from tgit.ui.settings_dialog import SettingsDialog
from tgit.ui.track_edition_page import TrackEditionPage
from tgit.ui.track_selection_dialog import TrackSelectionDialog
from tgit.ui.welcome_screen import welcome_screen as WelcomeScreen
from tgit.ui.main_window import main_window as MainWindow
from tgit.ui.album_screen import album_screen as AlbumScreen
# noinspection PyUnresolvedReferences
from tgit.ui import resources
from tgit.util import async_task_runner as task_runner


def show(widget):
    widget.show()


def centerOnScreen(widget):
    desktop = QApplication.desktop()
    position = widget.frameGeometry()
    position.moveCenter(desktop.availableGeometry().center())
    widget.move(position.topLeft())


def activate(widget):
    from PyQt5.QtCore import QSysInfo

    if hasattr(QSysInfo, "MacintoshVersion") and QSysInfo.MacintoshVersion > QSysInfo.MV_10_8:
        # Since Maverick, menu bar does not appear until the window is manually activated, so force
        # user to activate by not raising the window
        pass
    else:
        # we can safely raise the window
        widget.raise_()

    widget.activateWindow()


def showCenteredOnScreen(widget):
    show(widget)
    centerOnScreen(widget)
    activate(widget)


def AlbumCompositionPageController(dialogs, player, album):
    page = AlbumCompositionPage()
    page.addTracks.connect(lambda: dialogs.select_tracks(album).open())
    page.trackMoved.connect(lambda track, position: director.moveTrack(album, track, position))
    page.playTrack.connect(lambda track: director.playTrack(player, track))
    page.removeTrack.connect(lambda track: director.removeTrack(player, album, track))
    page.display(player, album)
    return page


def AlbumEditionPageController(dialogs, lookup_isni_dialog_factory, activity_indicator_dialog_factory,
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
    page = AlbumEditionPage(album, use_local_isni_backend)
    page.metadataChanged.connect(lambda metadata: director.updateAlbum(album, **metadata))
    page.selectPicture.connect(lambda: dialogs.select_picture(album).open())
    page.removePicture.connect(lambda: director.removeAlbumCover(album))
    page.lookupISNI.connect(lookup_isni)
    page.assignISNI.connect(assign_isni)
    page.clearISNI.connect(lambda: director.clearISNI(album))
    page.addPerformer.connect(add_performer)
    album.addAlbumListener(page)
    page.refresh()
    return page


def PerformerDialogController(parent, album):
    def assign_guest_performers():
        album.guestPerformers = dialog.getPerformers()

    dialog = PerformerDialog(parent)
    dialog.accepted.connect(assign_guest_performers)
    dialog.display(album.guestPerformers)
    dialog.open()
    return dialog


def ISNILookupDialogController(parent, album, identities):
    dialog = ISNILookupDialog(parent, identities)
    dialog.accepted.connect(lambda: director.selectISNI(dialog.selectedIdentity, album))
    dialog.open()
    return dialog


def ActivityIndicatorDialogController(parent):
    dialog = ActivityIndicatorDialog(parent)
    dialog.open()
    return dialog


def TrackEditionPageController(album, track):
    page = TrackEditionPage()
    page.metadataChanged.connect(lambda metadata: director.updateTrack(track, **metadata))

    class CancelSubscription(AlbumListener):
        def trackRemoved(self, removed, position):
            if removed == track:
                subscription.cancel()
                album.removeAlbumListener(page)

    subscription = track.metadata_changed.subscribe(page.display_track)
    album.addAlbumListener(page)
    album.addAlbumListener(CancelSubscription())
    page.display(album=album, track=track)
    return page


def make_picture_selection_dialog(parent_window, native, album):
    dialog = PictureSelectionDialog(parent_window, native)
    dialog.picture_selected.connect(lambda selection: director.changeAlbumCover(album, selection))
    return dialog


def SettingsDialogController(restartNotice, preferences, parent):
    dialog = SettingsDialog(parent)

    def save_preferences():
        preferences.add(**dialog.settings)
        dialog.close()
        restartNotice(parent).display()

    dialog.accepted.connect(save_preferences)
    dialog.add_language("en", dialog.tr("English"))
    dialog.add_language("fr", dialog.tr("French"))
    dialog.display(**preferences)
    return dialog


def make_export_as_dialog(parent_window, native, format_, album):
    dialog = ExportAsDialog(parent_window, native)
    dialog.export_as.connect(lambda destination: director.export_album(format_, album, destination, "windows-1252"))
    return dialog


def make_track_selection_dialog(parent, native, album):
    dialog = TrackSelectionDialog(parent, native)
    dialog.tracks_selected.connect(lambda selection: director.add_tracks_to_album(album, *selection))
    return dialog


def make_import_album_dialog(parent, native, album_portfolio):
    dialog = ImportAlbumFromTrackDialog(parent, native)
    dialog.track_selected.connect(lambda track_file: director.import_album(album_portfolio, track_file))
    return dialog


class Dialogs:
    _pictures = None
    _tracks = None
    _import = None
    _export = None

    def __init__(self, native):
        self.parent = None
        self._native = native

    def _picture_selection_dialog(self, album):
        if not self._pictures:
            self._pictures = make_picture_selection_dialog(self.parent, self._native, album)

        return self._pictures

    def _track_selection_dialog(self, album):
        if not self._tracks:
            self._tracks = make_track_selection_dialog(self.parent, self._native, album)

        return self._tracks

    def _import_selection_dialog(self, album_portfolio):
        if not self._import:
            self._import = make_import_album_dialog(self.parent, self._native, album_portfolio)

        return self._import

    def _export_album_dialog(self, album):
        if not self._export:
            self._export = make_export_as_dialog(self.parent, self._native, CsvFormat(), album)

        return self._export

    def select_picture(self, album):
        return self._picture_selection_dialog(album)

    def select_tracks(self, album):
        dialog = self._track_selection_dialog(album)
        dialog.select_files()
        dialog.filter_tracks(album.type)
        return dialog

    def select_tracks_in_folder(self, album):
        dialog = self._track_selection_dialog(album)
        dialog.select_folders()
        dialog.filter_tracks(album.type)
        return dialog

    def import_album(self, album_portfolio):
        return self._import_selection_dialog(album_portfolio)

    def export_album(self, album):
        return self._export_album_dialog(album)


def create_main_window(portfolio, player, preferences, name_registry, use_local_isni_backend, native):
    def show_settings_dialog():
        return SettingsDialogController(RestartMessageBox, preferences, window)

    def create_welcome_screen():
        return WelcomeScreen(dialogs, portfolio)

    def create_composition_page(album):
        return AlbumCompositionPageController(dialogs, player, album)

    def create_album_page(album):
        return AlbumEditionPageController(dialogs, show_isni_lookup_dialog,
                                          show_activity_indicator_dialog, show_performer_dialog,
                                          show_isni_assignation_failed_message_box, album, name_registry,
                                          use_local_isni_backend)

    def show_isni_lookup_dialog(album, identities):
        return ISNILookupDialogController(window, album, identities)

    def show_performer_dialog(album):
        return PerformerDialogController(window, album)

    def show_activity_indicator_dialog():
        return ActivityIndicatorDialogController(window)

    def show_isni_assignation_failed_message_box(details):
        isni_assignation_failed_message_box(window, details).open()

    def create_album_screen(album):
        def create_track_page(track):
            return TrackEditionPageController(album, track)

        return AlbumScreen(create_composition_page, create_album_page, create_track_page, album)

    dialogs = Dialogs(native)
    window = MainWindow(create_welcome_screen, create_album_screen, show_settings_dialog, dialogs, portfolio)
    dialogs.parent = window

    return window