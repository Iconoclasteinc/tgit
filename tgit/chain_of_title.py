from tgit.signal import signal, Signal


class ChainOfTitle:
    changed = signal(Signal.SELF)

    def __init__(self, **chain_of_title):
        self._publishers = chain_of_title.get("publishers", {})
        self._authors_composers = chain_of_title.get("authors_composers", {})

    @classmethod
    def from_track(cls, track):
        chain = cls()
        chain.update(lyricists=track.lyricist, composers=track.composer, publishers=track.publisher)
        return chain

    @property
    def contributors(self):
        return {"authors_composers": self._authors_composers, "publishers": self._publishers}

    def update(self, lyricists, composers, publishers):
        has_updated_authors_composers = self._update_authors_composers(composers, lyricists)
        has_updated_publishers = self._update_publishers(publishers)

        if has_updated_authors_composers or has_updated_publishers:
            self.changed.emit(self)

    def update_contributor(self, **contributor):
        self._try_update_contributor(contributor, self._authors_composers)
        self._try_update_contributor(contributor, self._publishers)

    def _update_publishers(self, publishers):
        has_updated = self._update_contributors(publishers, self._publishers)
        if has_updated:
            self._update_associated_publishers(publishers)

        return has_updated

    def _update_associated_publishers(self, publishers):
        def publisher_has_been_removed(author_composer):
            return "publisher" in author_composer.keys() and author_composer["publisher"] not in publishers

        for contributor in self._authors_composers.values():
            if publisher_has_been_removed(contributor):
                contributor["publisher"] = ""

    def _update_authors_composers(self, composers, lyricists):
        return self._update_contributors(lyricists + composers, self._authors_composers)

    @staticmethod
    def _update_contributors(new_contributors, contributors):
        to_remove = contributors.keys() - set(new_contributors)
        to_add = new_contributors - contributors.keys()
        for name in to_remove:
            del contributors[name]
        for name in to_add:
            contributors[name] = {"name": name}
        return len(to_remove) > 0 or len(to_add) > 0

    @staticmethod
    def _try_update_contributor(contributor, contributors):
        contributor_name = contributor["name"]
        if contributor_name in contributors:
            contributors[contributor_name] = contributor
