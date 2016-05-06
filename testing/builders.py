# -*- coding: utf-8 -*-

from tgit.album import Album
from tgit.auth import Session, User, Permission
from tgit.chain_of_title import ChainOfTitle
from tgit.metadata import Metadata, Image
from tgit.project_history import ProjectHistory, ProjectSnapshot
from tgit.project_studio import ProjectStudio
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


make_metadata = metadata


def track(filename="track.mp3", metadata_from=None, chain_of_title=None, **meta):
    new_track = Track(filename, metadata_from, chain_of_title)

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


def make_project(filename="project.tgit", type_="mp3", images=(), tracks=(), **meta):
    # Will eventually build a project, not an album
    return make_album(filename, of_type=type_, images=images, tracks=tracks, **meta)


def make_chain_of_title(authors_composers=None, publishers=None):
    auth = dict([(contributor["name"], contributor) for contributor in authors_composers or []])
    pub = dict([(contributor["name"], contributor) for contributor in publishers or []])
    return ChainOfTitle(authors_composers=auth, publishers=pub)


def make_snapshot(name="project", path="project.tgit", type_="mp3", cover_art=None):
    return ProjectSnapshot(name=name, type_=type_, path=path, cover_art=cover_art)


def make_project_history(*snapshots):
    return ProjectHistory(*snapshots)


def make_studio():
    return ProjectStudio()


def make_anonymous_user():
    return User.anonymous()


def make_registered_user(email="test@example.com", api_key="api-key", permissions=None):
    return User.registered_as(email, api_key, permissions or [Permission.lookup_isni.value])


def make_anonymous_session():
    return Session()


def make_registered_session(email="test@example.com", token="api-key", permissions=None):
    session = Session()
    session.login_as(email, token, permissions or [Permission.lookup_isni.value])
    return session


def make_preferences(locale="en", **prefs):
    preferences = UserPreferences()
    preferences.locale = locale
    for pref, value in prefs.items():
        setattr(preferences, pref, value)
    return preferences
