# -*- coding: utf-8 -*-
from tgit.album_portfolio import AlbumPortfolio

from tgit.metadata import Metadata, Image
from tgit.album import Album
from tgit.auth import Session, User
from tgit.track import Track


def image(mime='image/jpeg', data='...', type_=Image.OTHER, desc=''):
    return mime, data, type_, desc


def metadata(images=(), **meta):
    metadata = Metadata(**meta)

    for image in images:
        metadata.addImage(*image)

    return metadata


def track(filename='track.mp3', metadata=None, **meta):
    track = Track(filename, metadata)

    for tag, value in meta.items():
        setattr(track, tag, value)

    return track

make_track = track


def album(filename='album.tgit', of_type=Album.Type.FLAC, images=(), tracks=(), **meta):
    album = Album(filename=filename, of_type=of_type)

    for tag, value in meta.items():
        setattr(album, tag, value)

    for image in images:
        album.addImage(*image)

    for track in tracks:
        album.add_track(track)

    return album

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
