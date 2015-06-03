# -*- coding: utf-8 -*-
from hamcrest import assert_that, same_instance
import pytest

from test.util import builders as make
from tgit import album_director
from tgit.ui import Dialogs


@pytest.fixture()
def dialogs(qt):
    return Dialogs(album_director, native=True)


def test_creates_a_single_import_dialog_for_a_given_portfolio(dialogs):
    album_portfolio = make.album_portfolio()
    import_dialog = dialogs.import_album(album_portfolio)

    assert_that(dialogs.import_album(album_portfolio), same_instance(import_dialog))


def test_creates_a_single_save_as_dialog_for_a_given_portfolio(dialogs):
    album_portfolio = make.album_portfolio()
    save_as_dialog = dialogs.save_album_file(album_portfolio, of_type="mp3")

    assert_that(dialogs.save_album_file(album_portfolio, of_type="mp3"), same_instance(save_as_dialog))


def test_creates_a_single_picture_selection_dialog_for_a_given_album(dialogs):
    album = make.album()
    picture_dialog = dialogs.select_cover(album)

    assert_that(dialogs.select_cover(album), same_instance(picture_dialog))


def test_creates_a_new_picture_selection_dialog_for_each_album(dialogs):
    album = make.album()
    picture_dialog = dialogs.select_cover(album)
    dialogs.clear()

    assert_that(dialogs.select_cover(make.album()), not same_instance(picture_dialog))


def test_creates_a_single_track_selection_dialog_for_a_given_album(dialogs):
    album = make.album()
    track_dialog = dialogs.add_tracks(album)

    assert_that(dialogs.add_tracks(album), same_instance(track_dialog))
    assert_that(dialogs.add_tracks_in_folder(album), same_instance(track_dialog))


def test_creates_a_new_track_selection_dialog_for_each_album(dialogs):
    album = make.album()
    track_dialog = dialogs.add_tracks(album)
    dialogs.clear()

    assert_that(dialogs.add_tracks(make.album()), not same_instance(track_dialog))


def test_creates_a_single_export_dialog_for_a_given_album(dialogs):
    album = make.album()
    export_dialog = dialogs.export(album)

    assert_that(dialogs.export(album), same_instance(export_dialog))


def test_creates_a_new_export_dialog_for_each_album(dialogs):
    album = make.album()
    export_dialog = dialogs.export(album)
    dialogs.clear()

    assert_that(dialogs.export(make.album()), not same_instance(export_dialog))
