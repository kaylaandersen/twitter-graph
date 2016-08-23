import cypher

conn = "http://neo4j:IYWcb1ar2@ec2-54-197-153-60.compute-1.amazonaws.com:7474"


query = """MATCH p = (u1:User)<-[r:FOLLOWS]->(u2:User)-->
           WHERE u1.screen_name = 'BernieSanders'
           AND EXISTS(u2.following_added)
           RETURN relationships(p);"""
#
query_test = """MATCH p=()-[r:FOLLOWS]->()
                RETURN p LIMIT 50;"""

query_test = """MATCH
                p=(u1:User{screen_name:"BernieSanders"})-[r:FOLLOWS]->(u2:User)
                WHERE u1.screen_name = 'BernieSanders'
                AND EXISTS(u2.following_added)
                RETURN u2.screen_name, u3.screen_name;"""

query_path = """MATCH       p=(n:User{screen_name:'BernieSanders'})-[r1:FOLLOWS]->(m:User)-[r2:FOLLOWS]-(o:User)<-[r3:FOLLOWS]-(n:User{screen_name:'BernieSanders'}) RETURN p;"""

quey_test = """MATCH """

query_bernie = """MATCH (user)"""

query3 = """MATCH (c:User{screen_name : 'BernieSanders'})-[r:*0..1]-(d:User)
            WITH c, collect(r) as rs
            RETURN c, rs"""

result = cypher.run(query_test, conn=conn)
ig = IGraph.TupleList(result)

# closest betweeness
between = [(node["name"], node.betweenness()) for node in ig.vs]
