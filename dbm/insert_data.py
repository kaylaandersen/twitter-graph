from pprint import pprint
from py2neo import neo4j, node, rel

# hook into the graph database
db = neo4j.GraphDatabaseService('http://localhost:7474/db/data')

# insert data
# PASS note this is an example
def insert_data():
    die_hard = db.create(
        node({"name": "Bruce Willis"}),
        node({"name": "John McClane"}),
        node({"name": "Alan Rickman"}),
        node({"name": "Hans Gruber"}),
        node({"name": "Nakatomi Plaza"}),
        rel(0, "PLAYS", 1),
        rel(2, "PLAYS", 3),
        rel(1, "VISITS", 4),
        rel(3, "STEALS_FROM", 4),
        rel(1, "KILLS", 3),)
    pprint(die_hard)
