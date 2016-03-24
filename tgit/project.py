# -*- coding: utf-8 -*-
from tgit import local_storage


def load(studio, portfolio, from_catalog=local_storage):
    def load_project(filename):
        project = from_catalog.load_project(filename)
        studio.project_loaded(project)
        portfolio.add_album(project)

    return load_project
