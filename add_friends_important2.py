from datacollect import oauth, tgdb

if __name__ == '__main__':
    host_port = 'localhost'
    user = 'neo4j'
    password = 'IYWcb1ar2'
    json_file = 'galvanize_capstone1_token.json'
    # connect
    graph = tgdb.TwitterGraph(host_port, user, password)
    tapi = oauth.TwitterAPI(json_file)
    rel = 'FOLLOWING'
    users_missing_rel = graph.get_nodes_missing_rels_params()
    while users_missing_rel:
        users = tapi.get_users(users_missing_rel)
        for user in users:
            friend_chunk = user.friends_ids
            graph.add_following(user.id, friend_chunk, 0)
        count += len(friend_chunk)
        print 'Added {} friends'.format(len(friend_chunk))
        try:
            users_missing_rel = graph.get_nodes_missing_rels_params()
        except:
            print 'No nodes missing relation {}'.format(rel)
