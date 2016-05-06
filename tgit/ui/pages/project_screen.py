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
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

from tgit.signal import MultiSubscription
from tgit.ui.closeable import Closeable
from tgit.ui.helpers.ui_file import UIFile
from tgit.ui.observer import Observer


def make_project_screen(project, project_page, track_page):
    screen = ProjectScreen(project_page, track_page)

    subscriptions = MultiSubscription()
    subscriptions += project.track_inserted.subscribe(lambda index, track: screen.track_added(index, track, project))
    subscriptions += project.track_removed.subscribe(lambda position, track: screen.track_removed(position, project))
    subscriptions += project.track_moved.subscribe(lambda track, from_, to: screen.track_moved(from_, to, project))
    screen.closed.connect(lambda: subscriptions.cancel())

    screen.display(project)
    return screen


@Closeable
@Observer
class ProjectScreen(QWidget, UIFile):
    closed = pyqtSignal()

    _PROJECT_PAGE_INDEX, _TRACK_PAGES_STARTING_INDEX = range(2)

    def __init__(self, edit_project, edit_track):
        super().__init__()
        self._edit_project = edit_project
        self._edit_track = edit_track
        self._setup_ui()

    def _setup_ui(self):
        self._load(":/ui/project_screen.ui")
        self._pages.currentChanged.connect(self._update_navigation_controls)
        self._previous.clicked.connect(self._to_previous_page)
        self._next.clicked.connect(self._to_next_page)
        self._pages_navigation.activated.connect(self._to_page)

        self.addAction(self._quick_navigation_action)
        self._quick_navigation_action.triggered.connect(self._quick_navigate)

    def display(self, project):
        self._remove_all_pages()
        self._add_project_page(project)

        self._pages_navigation.addItem(self.tr("Project edition"), self._PROJECT_PAGE_INDEX)
        for index, track in enumerate(project.tracks):
            self.track_added(index, track, project)
        self._update_navigation_controls(0)

    def _add_project_page(self, project):
        self._insert_page(self._edit_project(project), self._PROJECT_PAGE_INDEX)

    def _quick_navigate(self):
        edit = self._pages_navigation.lineEdit()
        edit.setFocus()
        edit.selectAll()

    def track_added(self, index, track, project):
        self._insert_page(self._edit_track(track), self._track_page_index(index))
        self._rebuild_navigation_menu(project)
        self._update_navigation_controls(0)

    def track_removed(self, index, project):
        self._remove_page(self._track_page_index(index))
        self._rebuild_navigation_menu(project)
        self._update_navigation_controls(0)

    def track_moved(self, from_index, to_index, project):
        page = self._pages.widget(self._track_page_index(from_index))
        self._pages.removeWidget(page)
        self._pages.insertWidget(self._track_page_index(to_index), page)
        self._rebuild_navigation_menu(project)

    def _rebuild_navigation_menu(self, project):
        def format_name(track):
            return "{} - {}".format(track.track_number, track.track_title)

        def update_entry(track):
            self._pages_navigation.setItemText(self._index_of(track), format_name(track))

        def add_entry(track):
            self._pages_navigation.addItem(format_name(track))

        for index in reversed(range(self._TRACK_PAGES_STARTING_INDEX, self._pages_navigation.count())):
            self._pages_navigation.removeItem(index)

        for index, each_track in enumerate(project.tracks):
            self.unsubscribe(each_track.metadata_changed)
            add_entry(each_track)
            self.subscribe(each_track.metadata_changed, update_entry)

    def to_project_edition_page(self):
        self._to_page(self._PROJECT_PAGE_INDEX)

    def to_track_page(self, index):
        self._to_page(self._track_page_index(index))

    def _track_page_index(self, position):
        return self._TRACK_PAGES_STARTING_INDEX + position

    def _index_of(self, track):
        return self._track_page_index(track.track_number - 1)

    def _update_navigation_controls(self, index):
        self._previous.setDisabled(self._on_first_page())
        self._next.setDisabled(self._on_last_page())
        self._pages_navigation.setCurrentIndex(index)

    def _on_last_page(self):
        return self._on_page(self._page_count - 1)

    def _on_first_page(self):
        return self._on_page(0)

    def _on_page(self, index):
        return self.current_page == index

    def _insert_page(self, widget, position):
        self._pages.insertWidget(position, widget)

    def _remove_page(self, number):
        page = self._pages.widget(number)
        self._pages.removeWidget(page)
        page.setParent(None)
        page.close()

    @property
    def current_page(self):
        return self._pages.currentIndex()

    @property
    def _page_count(self):
        return self._pages.count()

    def _to_previous_page(self):
        self._to_page(self.current_page - 1)

    def _to_next_page(self):
        self._to_page(self.current_page + 1)

    def _to_page(self, number):
        self._pages.setCurrentIndex(number)

    def close(self):
        self._remove_all_pages()
        return True

    def _remove_all_pages(self):
        for index in reversed(range(self._page_count)):
            self._remove_page(index)
