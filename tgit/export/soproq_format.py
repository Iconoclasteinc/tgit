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
from datetime import date


def _to_duration(seconds):
    return seconds and "00:%02d:%02d" % divmod(round(seconds), 60) or ""


def _write_line(album, track, line_number, sheet):
    album_lead_performer = album.lead_performer if not album.compilation else "Artistes Variés"
    track_lead_performer = track.lead_performer if track.lead_performer else album_lead_performer
    recording_time = album.recording_time.split("-")[0] if album.recording_time else ""
    compilation = "O" if album.compilation else "N"

    sheet["A"+str(line_number)] = album.release_name    # TITRE ALBUM
    sheet["B"+str(line_number)] = album_lead_performer  # INTERPRÈTE ALBUM
    sheet["C"+str(line_number)] = ""                    # NATIONALITÉ INTERPRÈTE ALBUM
    sheet["D"+str(line_number)] = album.label_name      # MAISON DE DISQUES
    sheet["E"+str(line_number)] = album.label_name      # ÉTIQUETTE
    sheet["F"+str(line_number)] = ""                    # DISTRIBUTEUR
    sheet["G"+str(line_number)] = album.catalog_number  # NO. CATALOGUE
    sheet["H"+str(line_number)] = album.upc             # UPC
    sheet["I"+str(line_number)] = album.release_time    # DATE DE PUBLICATION
    sheet["J"+str(line_number)] = ""                    # RÉÉDITION
    sheet["K"+str(line_number)] = compilation           # COMPILATION
    sheet["L"+str(line_number)] = str(track.track_number)  # NO. PLAGE
    sheet["M"+str(line_number)] = track.track_title     # * TITRE ENREGISTREMENT SONORE
    sheet["N"+str(line_number)] = track_lead_performer  # * INTERPRÈTE ENREGISTREMENT SONORE
    sheet["O"+str(line_number)] = ""                    # * NATIONALITÉ INTERPRÈTE
    sheet["P"+str(line_number)] = track.isrc            # * ISRC
    sheet["Q"+str(line_number)] = _to_duration(track.duration)  # DURÉE
    sheet["R"+str(line_number)] = ""                    # * PAYS DE FIXATION
    sheet["S"+str(line_number)] = recording_time        # * ANNÉE DE FIXATION
    sheet["T"+str(line_number)] = album.artistic_producer  # * PRODUCTEUR INITIAL
    sheet["U"+str(line_number)] = ""                    # * NATIONALITÉ PRODUCTEUR
    sheet["V"+str(line_number)] = ""                    # * TYPE DE DROIT
    sheet["W"+str(line_number)] = ""                    # * POURCENTAGE
    sheet["X"+str(line_number)] = ""                    # * TYPE TERRITOIRE
    sheet["Y"+str(line_number)] = ""                    # * TERRITOIRE
    sheet["Z"+str(line_number)] = ""                    # DATE DÉBUT DE DROIT
    sheet["AA"+str(line_number)] = ""                   # DATE FIN DE DROIT


def _write_rights_holder_section(album, sheet):
    sheet["B6"] = album.label_name      # AYANT DROIT
    sheet["C6"] = str(date.today())     # DATE


def write(album, workbook):
    sheet = workbook.active
    _write_rights_holder_section(album, sheet)

    line_number = 13
    for track in album.tracks:
        _write_line(album, track, line_number, sheet)
        line_number += 1
