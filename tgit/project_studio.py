from tgit.signal import Observable
from tgit.signal import signal


class ProjectStudio(metaclass=Observable):
    project_opened = signal(str)

    _current_project = None

    @property
    def current_project(self):
        return self._current_project

    def project_loaded(self, project):
        self._current_project = project
        self.project_opened.emit(project)
