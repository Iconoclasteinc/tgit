# -*- coding: utf-8 -*-
from tgit import image
from tgit.signal import Observable, signal


def load_from(studio, store):
    history = store.load_history()
    studio.project_opened.subscribe(history.project_opened)
    history.history_changed.subscribe(lambda: store.store_history(history))
    return history


class ProjectSnapshot:
    THUMBNAIL_SIZE = (36, 36)

    @classmethod
    def of(cls, project, scaler=image):
        cover_thumbnail = scaler.scale(project.main_cover.data, *cls.THUMBNAIL_SIZE) if project.main_cover else None
        return cls(project.release_name, project.type, project.filename, cover_thumbnail)

    def __init__(self, name, type_, path, cover_art):
        self.name = name
        self.type_ = type_
        self.path = path
        self.cover_art = cover_art


class ProjectHistory(metaclass=Observable):
    history_changed = signal()

    def __init__(self, *past_projects):
        self._history = list(past_projects)

    def project_opened(self, project):
        self._history.insert(0, ProjectSnapshot.of(project))
        self.history_changed.emit()

    def __getitem__(self, index):
        return self._history[index]

    def __len__(self):
        return len(self._history)
