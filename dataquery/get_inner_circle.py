import cypher


cypherq = """MATCH (u1:User)<-[r:FOLLOWS]-(u2:User)
                             WHERE m.screen_name = 'BernieSanders'
                             AND NOT EXISTS(n.following_added)
                             RETURN n.id
                             LIMIT 100;"""

bernie_circle = """MATCH p=(m:User)-[r:FOLLOWS]->(n:User)
                   WHERE m.screen_name = 'BernieSanders'
                   AND n.following_added = True
                   RETURN p LIMIT 100;"""
