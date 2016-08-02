from datacollect import oauth, tgdb
import tweepy
from py2neo import Node

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
        for user_id in users_missing_rel:
            try:
                user_friends = tapi.get_friends_ids(user_id)
                count = 0
                for friend_chunk in user_friends:
                    graph.add_following(user_id, friend_chunk, count)
                    count += len(friend_chunk)
                print 'Added {} friends'.format(count)
            except tweep.TweepError as e:
                # some may not authorize you to get this
                error = e.args[0][0]['message']}
                user = Node('User', id=user_id)
                graph.graph.merge(node)
                user['followers_added'] = error
                graph.graph.push(user)

        try:
            users_missing_rel = graph.get_nodes_missing_rels_params()
        except:
            print 'No nodes missing relation {}'.format(rel)
