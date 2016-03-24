# -*- coding: utf-8 -*-
from tgit import fs
from tgit.signal import signal
from tgit.ui import locations


class ArtworkSelection:
    on_failure = signal(Exception)

    extensions = ["png", "jpeg", "jpg", "jpe"]
    initial_directory = locations.Pictures

    def __init__(self, project, preferences):
        self._preferences = preferences
        self._project = project

    @property
    def directory(self):
        try:
            return self._preferences.artwork_selection_folder
        except AttributeError:
            return self.initial_directory

    def artwork_loaded(self, image):
        self._project.remove_images()
        self._project.add_front_cover(*image)

    def directory_changed(self, directory):
        self._preferences.artwork_selection_folder = directory

    def failed(self, error):
        self.on_failure.emit(error)


def load(artwork_selection):
    def load_from(filename):
        try:
            mime = fs.guess_mime_type(filename)
            data = fs.read(filename)
            artwork_selection.artwork_loaded((mime, data))
        except Exception as e:
            artwork_selection.failed(e)

    return load_from
