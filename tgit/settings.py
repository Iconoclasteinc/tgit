# -*- coding: utf-8 -*
from tgit.auth import User
from tgit.metadata import Image
from tgit.project_history import ProjectHistory, ProjectSnapshot
from tgit.user_preferences import UserPreferences


class UserDataStore:
    def __init__(self, settings):
        self._settings = settings

    def load_user(self):
        self._settings.beginGroup('user')
        user = User(self._settings.value('email'), self._settings.value('api_key'), self._read_permissions())
        self._settings.endGroup()
        return user

    def store_user(self, user):
        self._settings.beginGroup("user")
        self._settings.setValue("email", user.email)
        self._settings.setValue("api_key", user.api_key)
        self._write_permissions(user.permissions)
        self._settings.endGroup()

    def remove_user(self):
        self._settings.remove("user")

    def _read_permissions(self):
        permissions = []
        size = self._settings.beginReadArray("permissions")
        for index in range(size):
            self._settings.setArrayIndex(index)
            permissions.append(self._settings.value("value"))
        self._settings.endArray()
        return permissions

    def _write_permissions(self, permissions):
        self._settings.beginWriteArray("permissions", size=len(permissions))
        for index in range(len(permissions)):
            self._settings.setArrayIndex(index)
            self._settings.setValue("value", permissions[index])
        self._settings.endArray()

    def close(self):
        self._settings.sync()


class PreferencesDataStore:
    def __init__(self, settings):
        self._settings = settings

    def load_preferences(self):
        preferences = UserPreferences()
        self._settings.beginGroup("preferences")
        if self._settings.contains("locale"):
            preferences.locale = self._settings.value("locale")
        self._settings.endGroup()
        return preferences

    def store_preferences(self, prefs):
        self._settings.beginGroup("preferences")
        self._settings.setValue("locale", prefs.locale)
        self._settings.endGroup()

    def remove_preferences(self):
        self._settings.remove("preferences")

    def close(self):
        self._settings.sync()


class HistoryDataStore:
    def __init__(self, settings):
        self._settings = settings

    def load_history(self):
        history = []
        if 'history' in self._settings.childGroups():
            history.extend(self._read_history())
        return ProjectHistory(*history)

    def store_history(self, history):
        self._write_history(history)

    def remove_history(self):
        self._settings.remove("history")

    def _read_history(self):
        history = []
        size = self._settings.beginReadArray("history")
        for index in range(size):
            self._settings.setArrayIndex(index)
            name = self._settings.value("name")
            path = self._settings.value("path")
            type_ = self._settings.value("type")
            cover_art = self._read_cover_art() if 'thumbnail' in self._settings.childGroups() else None
            history.append(ProjectSnapshot(name=name, path=path, type_=type_, cover_art=cover_art))
        self._settings.endArray()
        return history

    def _write_history(self, history):
        self._settings.beginWriteArray("history", size=len(history))
        for index in range(len(history)):
            past_project = history[index]
            self._settings.setArrayIndex(index)
            self._settings.setValue("name", past_project.name)
            self._settings.setValue("path", past_project.path)
            self._settings.setValue("type", past_project.type)
            if past_project.cover_art:
                self._write_cover_art(past_project)
        self._settings.endArray()

    def _read_cover_art(self):
        self._settings.beginGroup("thumbnail")
        mime = self._settings.value("mime_type")
        data = self._settings.value("data")
        type_= self._settings.value("type")
        desc = self._settings.value("description")
        self._settings.endGroup()
        return Image(mime, data, type_, desc)

    def _write_cover_art(self, past_project):
        self._settings.beginGroup("thumbnail")
        self._settings.setValue("mime_type", past_project.cover_art.mime)
        self._settings.setValue("data", past_project.cover_art.data)
        self._settings.setValue("type", past_project.cover_art.type)
        self._settings.setValue("description", past_project.cover_art.desc)
        self._settings.endGroup()

    def close(self):
        self._settings.sync()
