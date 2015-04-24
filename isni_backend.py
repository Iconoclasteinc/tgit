import random

from test.util import isni_database


class RandomIsniResponses():
    def __init__(self):
        self.actions = ["0000000080183206", "0000000121707484", "sparse", "invalid data"]

    def __next__(self):
        return self.actions[random.randint(0, len(self.actions) - 1)]


isni_database.persons["0000000080183206"] = [{"names": [("Joel", "Miller", "1969-")], "titles": ["Honeycombs"]}]
isni_database.organisations["0000000121707484"] = [{"names": [
    "The Beatles", "Beatles, The"], "titles": [
    "The fool on the hill from The Beatles' T.V. film Magical mystery tour"]}]
isni_database.assignation_generator = RandomIsniResponses()

isni_database.start()