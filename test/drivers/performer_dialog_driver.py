# -*- coding: utf-8 -*-
from cute.matchers import named, with_text
from ._screen_driver import ScreenDriver


class PerformerDialogDriver(ScreenDriver):
    def add_performer(self):
        self.button(with_text('ADD A PERFORMER')).click()

    def remove_performer(self, index):
        self.button(named('remove-performer-%(index)i' % locals())).click()

    def shows_ok_button(self, disabled=False):
        self.button(with_text('&OK')).is_disabled(disabled)

    def change_performer_name(self, name, index):
        self.lineEdit(named('performer-%(index)i' % locals())).replace_all_text(name)

    def change_instrument(self, instrument, index):
        self.lineEdit(named('instrument-%(index)i' % locals())).replace_all_text(instrument)

    def ok(self):
        self.button(with_text('OK')).click()

    def cancel(self):
        self.button(with_text('Cancel')).click()

    def shows_performers(self, performers):
        for index, performer in enumerate(performers):
            instrument, name = performer
            self.lineEdit(named('instrument-' + str(index))).has_text(instrument)
            self.lineEdit(named('performer-' + str(index))).has_text(name)