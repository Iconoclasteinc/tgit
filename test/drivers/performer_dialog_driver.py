# -*- coding: utf-8 -*-
from cute.matchers import named, with_text
from ._screen_driver import ScreenDriver
from cute.widgets import QDialogDriver
from tgit.ui.performer_dialog import FIRST_PERFORMER_ROW_INDEX


class PerformerDialogDriver(QDialogDriver, ScreenDriver):
    def add_performer(self, instrument, name, row):
        if row > FIRST_PERFORMER_ROW_INDEX:
            self.button(with_text("ADD A PERFORMER")).click()
        self.lineEdit(named("instrument_{0}".format(row))).replace_all_text(instrument)
        self.lineEdit(named("performer_{0}".format(row))).replace_all_text(name)

    def remove_performer(self, row):
        self.button(named("remove_performer_{0}".format(row))).click()

    def shows_ok_button(self, disabled=False):
        self.button(with_text("&OK")).is_disabled(disabled)

    def shows_performer(self, instrument, name, row):
        self.lineEdit(named("instrument_{0}".format(str(row)))).has_text(instrument)
        self.lineEdit(named("performer_{0}".format(str(row)))).has_text(name)
