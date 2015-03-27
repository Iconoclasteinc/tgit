from . import isni_database as server

server.database["00000001"] = [("Julien", "Clerc")]
server.database["00000002"] = [("Joel", "Miller")]
server.database["00000003"] = [("John", "Roney")]

server.start()