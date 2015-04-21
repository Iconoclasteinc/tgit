#!/usr/bin/env python

from tgit.audio import MediaPlayer
from tgit.tagger import TGiT
from tgit.isni.name_registry import NameRegistry


def main():
    name_registry = NameRegistry(host='isni-m.oclc.nl',
                                 assign_host='isni-m-acc.oclc.nl',
                                 secure=True,
                                 username='ICON',
                                 password='crmeoS4d')

    app = TGiT(MediaPlayer, name_registry)
    app.setApplicationName('TGiT')
    app.setOrganizationName('Iconoclaste Inc.')
    app.setOrganizationDomain('tagyourmusic.com')
    app.launch()


if __name__ == "__main__":
    main()