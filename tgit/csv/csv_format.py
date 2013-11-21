# -*- coding: utf-8 -*-

import csv
import functools as func


def toPeopleList(people):
    return people and '; '.join(['%s: %s' % (role, name) for role, name in people]) or ''


class CsvFormat(object):
    # todo pass a dictionary responsible for translation rather than hardcoding header names
    Headers = ["Titre de l'album", "Nom de l'artiste principal", "Musiciens de l'album",
               "Nom de la maison de disques", u'Numéro de catalogue', 'UPC/EAN', 'Commentaires',
               u"Date de mise en marché de l'album", "Date de l'enregistrement",
               "Studios d'enregistrement", u'Réalisateur', 'Mixeur',
               'Titre de la piste', 'Infos sur la version', u'Invité spécial', 'Paroles',
               'Langue des paroles', u'Éditeur', 'Auteur', 'Compositeur', 'ISRC', 'Tags']

    def __init__(self, encoding):
        self._encoding = encoding

    def write(self, album, out):
        writer = csv.writer(out)
        self.writeHeader(writer)
        for track in album.tracks:
            self.writeRecord(writer, album, track)

    def writeHeader(self, writer):
        writer.writerow(self._encode(self.Headers))

    def writeRecord(self, writer, album, track):
        row = album.releaseName, album.leadPerformer, toPeopleList(album.guestPerformers), \
            album.labelName, album.catalogNumber, album.upc, album.comments, \
            album.releaseTime, album.recordingTime, album.recordingStudios, album.producer, \
            album.mixer, track.trackTitle, track.versionInfo, track.featuredGuest, \
            track.lyrics, track.language, track.publisher, track.lyricist, track.composer, \
            track.isrc, track.tags
        writer.writerow(self._encode(row))

    def _encode(self, texts):
        return map(toExcelNewLines, map(func.partial(encodeAs, self._encoding), texts))


def toExcelNewLines(text):
    return text.replace('\n', '\r')


def encodeAs(encoding, text):
    return text and text.encode(encoding) or ''
