



cypherq = """MATCH (n:User)<-[r:FOLLOWS]-(m:User)
                             WHERE m.screen_name = 'BernieSanders'
                             AND NOT EXISTS(n.following_added)
                             RETURN n.id
                             LIMIT 100;"""
