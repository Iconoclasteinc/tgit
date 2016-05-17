from xml.etree import ElementTree

__author__ = 'Jonathan'


class Party:
    """
    Supported: PartyId (ISNI), FullName, IsOrganization
    Not Supported:
        FullNameAsciiTranscribed, FullNameIndexed, NamesBeforeKeyName, KeyName, NamesAfterKeyName, AbbreviatedName,
        PostalAddress, PhoneNumber, EmailAddress, Nationality
    """

    def __init__(self, sequence, full_name, isni=None, is_organization=False):
        self._sequence = sequence
        self._is_organisation = str(is_organization).lower()
        self._isni = isni
        self._full_name = full_name

    @property
    def reference(self):
        return "P-{0:05d}".format(self._sequence)

    def write_to(self, root):
        party_element = ElementTree.SubElement(root, "Party")

        party_reference = ElementTree.SubElement(party_element, "PartyReference")
        party_reference.text = self.reference

        if self._isni:
            party_id = ElementTree.SubElement(party_element, "PartyId", IsISNI=str(True).lower())
            isni = ElementTree.SubElement(party_id, "ISNI")
            isni.text = self._isni

        party_name = ElementTree.SubElement(party_element, "PartyName")
        full_name = ElementTree.SubElement(party_name, "FullName")
        full_name.text = self._full_name

        is_organization = ElementTree.SubElement(party_element, "IsOrganization")
        is_organization.text = str(self._is_organisation)


class PartyList:
    def __init__(self, parties):
        self._parties = parties

    def write_to(self, root):
        party_list_element = ElementTree.SubElement(root, "PartyList")
        for party in self._parties.values():
            party.write_to(party_list_element)

    def reference_for(self, name):
        return self._parties[name].reference if name in self._parties else None

    @classmethod
    def from_(cls, project):
        def add_party(name, is_organization=False):
            if name and name not in parties:
                parties[name] = Party(len(parties), name, isnis.get(name), is_organization)

        isnis = project.isnis or {}

        parties = {}
        add_party(project.lead_performer)
        add_party(project.label_name, is_organization=True)
        for _, musician in project.guest_performers or []:
            add_party(musician)

        for track in project.tracks:
            add_party(track.lead_performer)
            add_party(track.featured_guest)
            add_party(track.music_producer)
            add_party(track.mixer)
            add_party(track.recording_studio, is_organization=True)
            add_party(track.production_company, is_organization=True)
            for lyricist in track.lyricist or []:
                add_party(lyricist)
            for composer in track.composer or []:
                add_party(composer)
            for publisher in track.publisher or []:
                add_party(publisher, is_organization=True)

        return cls(parties)