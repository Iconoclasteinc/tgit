#!/usr/bin/env python

from PyQt5.QtCore import QSettings

from tgit.audio.player import MediaPlayer
from tgit.tagger import TGiT
from tgit.isni.name_registry import NameRegistry
from tgit.preferences import Preferences


def main():
    name_registry = NameRegistry(host='isni-m.oclc.nl',
                                 assignHost='isni-m-acc.oclc.nl',
                                 secure=True,
                                 username='ICON',
                                 password='crmeoS4d')

    app = TGiT(MediaPlayer, name_registry)
    app.setApplicationName('TGiT')
    app.launch(Preferences(QSettings('tagtamusique.com', 'TGiT')))


if __name__ == "__main__":
    main()