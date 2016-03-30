# -*- coding: utf-8 -*-
from tgit.signal import Observable, signal


def load_from(studio, store):
    history = store.load_history()
    studio.project_opened.subscribe(history.project_opened)
    history.history_changed.subscribe(lambda: store.store_history(history))
    return history


class ProjectHistory(metaclass=Observable):
    history_changed = signal()

    def __init__(self, *past_projects):
        self._history = list(past_projects)

    def project_opened(self, project):
        self._history.insert(0, project)
        self.history_changed.emit()

    def __getitem__(self, index):
        return self._history[index]

    def __len__(self):
        return len(self._history)
