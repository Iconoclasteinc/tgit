# -*- coding: utf-8 -*-
from PyQt5.QtCore import QLocale

from tgit.album import Album
from tgit.album_portfolio import AlbumPortfolio
from tgit.auth import Session, User
from tgit.metadata import Metadata, Image
from tgit.track import Track
from tgit.user_preferences import UserPreferences


def image(mime="image/jpeg", data="...", type_=Image.OTHER, desc=""):
    return mime, data, type_, desc


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


def album_portfolio():
    return AlbumPortfolio()


def make_anonymous_user():
    return User.anonymous()


def make_registered_user(email="test@example.com", token="api-key"):
    return User.registered_as(email, token)


def make_anonymous_session():
    return Session()


def make_registered_session(email="test@example.com", token="api-key"):
    session = Session()
    session.login_as(email, token)
    return session


def make_preferences(locale="en"):
    preferences = UserPreferences()
    preferences.locale = QLocale(locale)
    return preferences
