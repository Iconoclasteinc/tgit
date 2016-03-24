# -*- coding: utf-8 -*-
from PyQt5.QtCore import QLocale

from tgit.album import Album
from tgit.album_portfolio import AlbumPortfolio
from tgit.auth import Session, User, Permission
from tgit.metadata import Metadata, Image
from tgit.project_history import ProjectHistory
from tgit.track import Track
from tgit.user_preferences import UserPreferences


def image(mime="image/jpeg", data="...", type_=Image.OTHER, desc=""):
    return mime, data, type_, desc


make_image = image


def metadata(images=(), **meta):
    new_metadata = Metadata(**meta)

    for current_image in images:
        new_metadata.addImage(*current_image)

    return new_metadata


def track(filename="track.mp3", metadata_from=None, **meta):
    new_track = Track(filename, metadata_from)

    for tag, value in meta.items():
        setattr(new_track, tag, value)

    return new_track


make_track = track


def album(filename="album.tgit", of_type=Album.Type.FLAC, images=(), tracks=(), **meta):
    new_album = Album(filename=filename, of_type=of_type)

    for tag, value in meta.items():
        setattr(new_album, tag, value)

    for current_image in images:
        new_album.add_image(*current_image)

    for current_track in tracks:
        new_album.add_track(current_track)

    return new_album


make_album = album


def make_portfolio(project=None):
    portfolio = AlbumPortfolio()
    if project is not None:
        portfolio.add_album(project)
    return portfolio


def make_project_history(*past_projects):
    history = ProjectHistory()
    for past_project in past_projects:
        history.project_opened(past_project)

    return history


def make_anonymous_user():
    return User.anonymous()


def make_registered_user(email="test@example.com", token="api-key", permissions=None):
    return User.registered_as(email, token, permissions or [Permission.lookup_isni.value])


def make_anonymous_session():
    return Session()


def make_registered_session(email="test@example.com", token="api-key", permissions=None):
    session = Session()
    session.login_as(email, token, permissions or [Permission.lookup_isni.value])
    return session


def make_preferences(locale="en"):
    preferences = UserPreferences()
    preferences.locale = QLocale(locale)
    return preferences
