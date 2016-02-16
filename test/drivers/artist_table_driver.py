from ._screen_driver import ScreenDriver
from cute.matchers import named, with_text
from tgit.ui.pages.album_edition_page import MusicianRow, MusicianTable


def musician_table_driver(parent):
    return MusicianTableDriver.find_single(parent, MusicianTable, named("_musician_table_container"))


class MusicianTableDriver(ScreenDriver):
    def shows_only_musicians_in_table(self, *musicians):
        for index, musician in enumerate(musicians):
            instrument, name = musician
            self.lineEdit(with_text(instrument)).exists()
            self.lineEdit(with_text(name)).exists()

    def remove_musician(self, row):
        musician_row_driver(self, row - 1).remove_musician()

    def add_musician(self, instrument, name, row):
        musician_row_driver(self, row - 1).change_instrument(instrument)
        musician_row_driver(self, row - 1).change_musician_name(name)

    def change_instrument_of_row(self, row, text):
        musician_row_driver(self, row - 1).change_instrument(text)

    def change_musician_of_row(self, row, text):
        musician_row_driver(self, row - 1).change_musician_name(text)


def musician_row_driver(parent, index):
    return MusicianRowDriver.find_single(parent, MusicianRow, named("_musician_row_" + str(index)))


class MusicianRowDriver(ScreenDriver):
    def shows_musician(self, instrument, name):
        self.lineEdit(with_text(instrument)).exists()
        self.lineEdit(with_text(name)).exists()

    def remove_musician(self):
        self.button(named("_remove_musician_button")).click()

    def add_musician(self, instrument, name):
        self.lineEdit(named("_instrument")).change_text(instrument)
        self.lineEdit(named("_musician_name")).change_text(name)

    def change_instrument(self, text):
        self.lineEdit(named("_instrument")).change_text(text)

    def change_musician_name(self, text):
        self.lineEdit(named("_musician_name")).change_text(text)