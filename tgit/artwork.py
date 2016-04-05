# -*- coding: utf-8 -*-
from tgit import fs
from tgit.signal import signal


class ArtworkSelection:
    on_failure = signal(Exception)

    extensions = ["png", "jpeg", "jpg", "jpe"]

    def __init__(self, project, preferences):
        self._preferences = preferences
        self._project = project

    @property
    def directory(self):
        return self._preferences.artwork_location

    def artwork_loaded(self, image):
        self._project.remove_images()
        self._project.add_front_cover(*image)

    def directory_changed(self, directory):
        self._preferences.artwork_location = directory

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
