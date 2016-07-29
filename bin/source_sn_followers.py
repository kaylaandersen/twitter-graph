from datacollect import graph_links

if __name__ == '__main__':
    host_port = 'localhost'
    user = 'neo4j'
    password = 'IYWcb1ar2'
    json_file = 'galvanize_capstone1_token.json'
    source_sn = 'BernieSanders'
    graph_links.tgdb_walk(host_port, user, password, json_file, 'FOLLOWERS', source_sn)
    print 'Done!'
