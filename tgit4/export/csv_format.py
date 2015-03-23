# -*- coding: utf-8 -*-

import csv

from PyQt4.QtCore import QObject


def toBoolean(value):
    return value and 'True' or 'False'


def toPeopleList(people):
    return people and '; '.join(['%s: %s' % (role, name) for role, name in people]) or ''


class CsvFormat(QObject):
    Headers = ['Album Title', 'Compilation', 'Lead Performer', 'Lead Performer ISNI', 'Guest Performers', 'Label Name',
               'Catalog Number',
               'UPC/EAN', 'Comments', 'Release Date', 'Recording Date', 'Recording Studios', 'Producer', 'Mixer',
               'Primary Style', 'Track Title', 'Version Information', 'Featured Guest', 'Lyrics', 'Language',
               'Publisher', 'Lyricist', 'Composer', 'ISRC', 'Tags']

    def __init__(self, encoding):
        QObject.__init__(self)
        self.encoding = encoding

    def write(self, album, out):
        writer = csv.writer(out)
        self.writeHeader(writer)
        for track in album.tracks:
            self.writeRecord(writer, album, track)

    def writeHeader(self, writer):
        writer.writerow(self.encodeRow(self.Headers))

    def writeRecord(self, writer, album, track):
        row = album.releaseName, toBoolean(album.compilation), track.leadPerformer, album.isni, \
              toPeopleList(album.guestPerformers), album.labelName, album.catalogNumber, album.upc, album.comments, \
              album.releaseTime, album.recordingTime, album.recordingStudios, album.producer, \
              album.mixer, album.primaryStyle, track.trackTitle, track.versionInfo, track.featuredGuest, \
              track.lyrics, track.language, track.publisher, track.lyricist, track.composer, \
              track.isrc, track.labels
        writer.writerow(self.encodeRow(row))

    def encode(self, text):
        return text.encode(self.encoding)

    def translate(self, text):
        return text and self.tr(text) or ''

    def encodeRow(self, texts):
        return map(toExcelNewLines, map(self.encode, map(self.translate, texts)))


def toExcelNewLines(text):
    return text.replace('\n', '\r')
