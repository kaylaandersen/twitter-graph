from datacollect import oauth, tgdb
import time

def tgdb_walk(host_port, user, password, json_file, rel, source_sn=None):
    """Valid input for rel is 'FOLLOWING' or 'FOLLOWERS'"""
    graph = tgdb.TwitterGraph(host_port, user, password)
    # connect to twitter API
    tapi = oauth.TwitterAPI(json_file)
    if source_sn:
        user_id = tapi.get_user(screen_name=source_sn).id # get source user id
    else:
        # get first user node missing relationship
        user_id = graph.get_nodes_missing_rels(rel)
    # add links for the given user and relationship
    # if there is a source user screen name, only pass once
    # otherwise, will add links for all the users missing relationship
    while user_id:
        if rel == 'FOLLOWING':
            user_friends = tapi.get_friends_ids(user_id)
            for friend_chunk in user_friends:
                graph.add_following(user, friend_chunk)
            print 'added friends'
        elif rel == 'FOLLOWERS':
            print 'waiting on followers'
            user_followers = tapi.get_followers_ids(user_id)
            for follower_chunk in user_followers:
                print 'adding followers...'
                graph.add_followers(user_id, follower_chunk)
                time.sleep(180)
        else:
            print "what"
        # don't conitnue to iterate if this is the source user
        if source_sn:
            break
        else:
            user_id = graph.get_nodes_missing_rels(rel)
