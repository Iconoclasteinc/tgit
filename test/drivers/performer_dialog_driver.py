# -*- coding: utf-8 -*-
from cute.matchers import named, with_text
from ._screen_driver import ScreenDriver
from cute.widgets import QDialogDriver
from tgit.ui.performer_dialog import FIRST_PERFORMER_ROW_INDEX


class PerformerDialogDriver(QDialogDriver, ScreenDriver):
    def add_performer(self):
        self.button(with_text("ADD A PERFORMER")).click()

    def remove_performer(self, index):
        self.button(named("remove_performer_{0}".format(index + FIRST_PERFORMER_ROW_INDEX))).click()

    def shows_ok_button(self, disabled=False):
        self.button(with_text("&OK")).is_disabled(disabled)

    def change_performer_name(self, name, index):
        self.lineEdit(named("performer_{0}".format(index + FIRST_PERFORMER_ROW_INDEX))).replace_all_text(name)

    def change_instrument(self, instrument, index):
        self.lineEdit(named("instrument_{0}".format(index + FIRST_PERFORMER_ROW_INDEX))).replace_all_text(instrument)

    def shows_performers(self, performers):
        for index, performer in enumerate(performers):
            instrument, name = performer
            self.lineEdit(named("instrument_{0}".format(str(index + FIRST_PERFORMER_ROW_INDEX)))).has_text(instrument)
            self.lineEdit(named("performer_{0}".format(str(index + FIRST_PERFORMER_ROW_INDEX)))).has_text(name)
