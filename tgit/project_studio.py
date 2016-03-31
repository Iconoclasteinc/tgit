from tgit.album import Album
from tgit.signal import Observable
from tgit.signal import signal


class ProjectStudio(metaclass=Observable):
    on_project_opened = signal(Album)
    on_project_saved = signal(Album)

    _current_project = None

    @property
    def current_project(self):
        return self._current_project

    def project_loaded(self, project):
        self._current_project = project
        self.on_project_opened.emit(project)

    project_created = project_loaded

    def project_saved(self, project):
        self.on_project_saved.emit(project)
