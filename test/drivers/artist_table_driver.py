from ._screen_driver import ScreenDriver
from cute.matchers import named, with_text
from tgit.ui.pages.album_edition_page import ArtistRow, ArtistsTable


def artist_table_driver(parent):
    return ArtistTableDriver.find_single(parent, ArtistsTable, named("_artists_table_container"))


class ArtistTableDriver(ScreenDriver):
    def shows_only_artists_in_table(self, *artists):
        for index, artist in enumerate(artists):
            instrument, name = artist
            self.lineEdit(with_text(instrument)).exists()
            self.lineEdit(with_text(name)).exists()

    def remove_artist(self, row):
        artist_row_driver(self, row - 1).remove_artist()

    def add_artist(self, instrument, name, row):
        artist_row_driver(self, row - 1).change_instrument(instrument)
        artist_row_driver(self, row - 1).change_artist_name(name)

    def change_instrument_of_row(self, row, text):
        artist_row_driver(self, row - 1).change_instrument(text)

    def change_artist_of_row(self, row, text):
        artist_row_driver(self, row - 1).change_artist_name(text)


def artist_row_driver(parent, index):
    return ArtistRowDriver.find_single(parent, ArtistRow, named("_artist_row_" + str(index)))


class ArtistRowDriver(ScreenDriver):
    def shows_artist(self, instrument, name):
        self.lineEdit(with_text(instrument)).exists()
        self.lineEdit(with_text(name)).exists()

    def remove_artist(self):
        self.button(named("_remove_artist_button")).click()

    def add_artist(self, instrument, name):
        self.lineEdit(named("_instrument")).change_text(instrument)
        self.lineEdit(named("_artist_name")).change_text(name)

    def change_instrument(self, text):
        self.lineEdit(named("_instrument")).change_text(text)

    def change_artist_name(self, text):
        self.lineEdit(named("_artist_name")).change_text(text)
