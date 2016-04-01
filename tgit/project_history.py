# -*- coding: utf-8 -*-
from collections import deque

from tgit import imager
from tgit.signal import Observable, signal


def load_from(studio, store):
    history = store.load_history()
    studio.on_project_opened.subscribe(history.project_opened)
    studio.on_project_saved.subscribe(history.project_saved)
    history.on_history_changed.subscribe(lambda: store.store_history(history))
    return history


class ProjectSnapshot:
    THUMBNAIL_SIZE = (64, 64)

    @classmethod
    def of(cls, project, image_editor=imager):
        thumbnail = image_editor.scale(project.main_cover, *cls.THUMBNAIL_SIZE) if project.main_cover else None
        return cls(project.release_name, project.type, project.filename, thumbnail)

    def __init__(self, name, type_, path, cover_art):
        self.name = name
        self.type = type_
        self.path = path
        self.cover_art = cover_art

    def __repr__(self):
        return "ProjectHistory(name='{name}', type_='{type}', path='{path}')".format(
            name=self.name, type=self.type, path=self.path)


class ProjectHistory(metaclass=Observable):
    on_history_changed = signal()

    def __init__(self, *past_projects):
        self._history = deque(past_projects, maxlen=10)

    def project_opened(self, project):
        self._add_to_history(project)

    def project_saved(self, project):
        self._add_to_history(project)

    def _add_to_history(self, project):
        stale_entry = self._snapshot_for(project)
        if stale_entry is not None:
            self._history.remove(stale_entry)
        self._history.appendleft(ProjectSnapshot.of(project))
        self.on_history_changed.emit()

    def _snapshot_for(self, project):
        return next(filter(lambda entry: entry.path == project.filename, self._history), None)

    def __getitem__(self, index):
        return self._history[index]

    def __len__(self):
        return len(self._history)
