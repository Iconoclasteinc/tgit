# -*- coding: utf-8 -*-
#
# TGiT, Music Tagger for Professionals
# Copyright (C) 2013 Iconoclaste Musique Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

from tgit.ui.dialogs.about_dialog import AboutDialog


class MessageBoxes:
    def __init__(self, confirm_before_exiting, get_parent):
        self._get_parent = get_parent
        self._confirm_before_exiting = confirm_before_exiting

    @property
    def _parent(self):
        return self._get_parent()

    @staticmethod
    def _open(message):
        message.open()
        return message

    def load_album_failed(self, error):
        return self._open(MessageBox.warn(self._parent,
                                          "The album file you selected cannot be loaded.",
                                          "The file might be corrupted or part of the album content cannot be found."))

    def save_album_failed(self, error):
        return self._open(MessageBox.warn(self._parent,
                                          "Your album file could not be saved.",
                                          "Please check that you have permission to write to the album's location."))

    def restart_required(self):
        return self._open(MessageBox.inform(self._parent, "You need to restart TGiT for changes to take effect."))

    def isni_assignation_failed(self, details=None):
        return self._open(MessageBox.warn(self._parent, "Could not assign an ISNI", details=details))

    def cheddar_connection_failed(self):
        return self._open(MessageBox.warn(self._parent,
                                          "Unable to connect to TGiT remote server.",
                                          "Please try again later."))

    def cheddar_authentication_failed(self):
        return self._open(MessageBox.warn(self._parent,
                                          "Could not authenticate you to the TGiT remote server.",
                                          "Please sign out and sign back in to fix this issue."))

    def permission_denied(self):
        return self._open(MessageBox.warn(self._parent,
                                          "You don't have the required permission or you might have exceeded the limit "
                                          "of your plan.",
                                          "Please upgrade your subscription's plan."))

    def export_failed(self, error):
        return self._open(MessageBox.warn(self._parent,
                                          "Could not export your album.",
                                          "Please check that you have permission to write to the album's location."))

    def close_album_confirmation(self, **handlers):
        return self._open(
            ConfirmationBox.warn(self._parent,
                                 "You are about to close the current album. Are you sure you want to continue?",
                                 "Make sure to save your work before closing the album. "
                                 "Any unsaved work will be lost.",
                                 yes_button_text="Close",
                                 **handlers))

    def overwrite_album_confirmation(self, **handlers):
        return self._open(ConfirmationBox.warn(self._parent,
                                               "This album already exists. Do you want to replace it?",
                                               "A file with the same name already exists at the location you specified."
                                               " Replacing it will overwrite its current contents.",
                                               yes_button_text="Replace",
                                               **handlers))

    def confirm_exit(self):
        if not self._confirm_before_exiting:
            return True

        box = ConfirmationBox.warn(self._parent,
                                   "You are about to quit TGiT. Are you sure you want to continue?",
                                   "Make sure to save your work before you quit TGiT. "
                                   "Any unsaved work will be lost.",
                                   yes_button_text="Quit")
        box.setWindowModality(Qt.WindowModal)
        return box.exec() == QMessageBox.Yes

    def warn_soproq_default_values(self):
        return self._open(MessageBox.warn(self._parent,
                                          "SOPROQ declaration file was generated with default values.",
                                          "The form was filled with default values assuming you own the rights of the"
                                          " recordings covered by this declaration, forever and throughout the "
                                          "world.\n\nIf this is not the case, please manually review the declaration "
                                          "file."))

    def about_qt(self):
        QMessageBox().aboutQt(self._parent)

    def about_tgit(self):
        return self._open(AboutDialog(self._parent))


class MessageBox(QMessageBox):
    def __init__(self, parent, message, information, icon, details):
        super().__init__(parent)
        self.setObjectName("message_box")
        self.setText(self.tr(message))
        self.setInformativeText(self.tr(information))
        self.setModal(True)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setDetailedText(details)
        self.setStandardButtons(QMessageBox.Ok)
        self.setDefaultButton(QMessageBox.Ok)
        self.setIcon(icon)

    @classmethod
    def inform(cls, parent, message, information=None, details=None, **handlers):
        return cls(parent, message, information, QMessageBox.NoIcon, details, **handlers)

    @classmethod
    def warn(cls, parent, message, information=None, details=None, **handlers):
        return cls(parent, message, information, QMessageBox.Warning, details, **handlers)


class ConfirmationBox(MessageBox):
    _on_accept = lambda _: None

    def __init__(self, parent, message, information, icon, details=None, **handlers):
        super().__init__(parent, message, information, icon, details)

        self.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        self.buttonClicked.connect(self._button_clicked)
        self._register_signal_handlers(handlers)

    def on_accept(self, on_accept):
        self._on_accept = on_accept

    def yes_button_text(self, text):
        self.button(QMessageBox.Yes).setText(self.tr(text))

    def _register_signal_handlers(self, handlers):
        for name, handler in handlers.items():
            getattr(self, name)(handler)

    def _button_clicked(self, button):
        role = self.buttonRole(button)

        if role == QMessageBox.YesRole:
            self._on_accept()
