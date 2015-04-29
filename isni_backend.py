import random

from test.util import isni_database

isni_database.persons["0000000080183206"] = [
    {"names": [("Joel", "Miller", "1969-")], "titles": ["--and then everything started to look different--"]}
]

isni_database.persons["0000000080183206"] = [
    {"names": [("Joel", "Miller", "")], "titles": ["Size matters : how big government puts the squeeze on America's families, finances, and freedom (and limits the pursuit of happiness)"]}
]

isni_database.persons["0000000384226711"] = [
    {"names": [("Joel", "Miller", "1975-")], "titles": ["The Patent Trial and Appeal Board : advocacy and practice"]}
]

isni_database.persons["0000000067123073"] = [
    {"names": [("Joel E.", "Miller", "")], "titles": ["Modern trust forms and checklists : with commentary : based in part on an earlier work prepared by James G. Hellmuth"]}
]

isni_database.persons["0000000030415486"] = [
    {"names": [("Joel R.", "Miller", "")], "titles": ["Drug abuse prevention in Atlantic County ; a status report of school based prevention practices as viewed by secondary school principals"]}
]

isni_database.persons["0000000030415486"] = [
    {"names": [("Joel S.", "Miller", "")], "titles": ["Chemically modified surfaces in catalysis and electrocatalysis based on a symposium jointly sponsored by the Divisions of Inorganic, Analytical and Petroleum Chemistry at the 182nd ACS National Meeting, New York, New York, August 23-25, 1981"]}
]

isni_database.persons["0000000029259914"] = [
    {"names": [("Joel William", "Miller", "1955-")], "titles": ["The chromatographic characterization of halogenated organics formed in the chlorination of aquatic humic substances"]}
]

isni_database.organisations["0000000121707484"] = [
    {"names": ["The Beatles", "Beatles, The"], "titles": ["The fool on the hill from The Beatles' T.V. film Magical mystery tour"]}
]

isni_database.assignation_actions["Joel Miller"] = "0000000080183206"
isni_database.assignation_actions["John Roney"] = "invalid data"
isni_database.assignation_actions["Rebecca Ann Maloy"] = "sparse"

isni_database.start()