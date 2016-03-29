class FakeIdentitySelection:
    identities = None
    identity = None
    error = None
    has_started = False

    def __init__(self, name=None, *works):
        self.person = name
        self.works = list(works)

    def identities_found(self, identities):
        self.identities = identities

    def failed(self, error):
        self.error = error

    def identity_selected(self, identity_):
        self.identity = identity_

    def identity_assigned(self, identity_):
        self.identity = identity_

    def lookup_started(self):
        self.has_started = True

    def assignation_started(self):
        self.has_started = True


class FakeIdentitySelectionListener:
    identities = {}
    error = None
    is_started = False
    is_connection_failed = False
    is_permission_denied = False
    is_success = False

    def identities_available(self, identities):
        self.identities = identities

    def failed(self, error):
        self.error = error

    def connection_failed(self):
        self.is_connection_failed = True

    def permission_denied(self):
        self.is_permission_denied = True

    def success(self):
        self.is_success = True

    def started(self):
        self.is_started = True
