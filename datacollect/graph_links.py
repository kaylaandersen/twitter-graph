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
        try:
            # get first user node missing relationship
            user_id = graph.get_nodes_missing_rels(rel)[0]
        except:
            print 'No nodes missing relation {}'.format(rel)
            break
    # add links for the given user and relationship
    # if there is a source user screen name, only pass once
    # otherwise, will add links for all the users missing relationship
    while user_id:
        if rel == 'FOLLOWING':
            user_friends = tapi.get_friends_ids(user_id)
            count = 0
            for friend_chunk in user_friends:
                graph.add_following(user_id, friend_chunk, count)
                count += len(friend_chunk)
            print 'Added {} friends'.format(count)
        elif rel == 'FOLLOWERS':
            print 'waiting on followers'
            count = 0
            user_followers = tapi.get_followers_ids(user_id)
            for follower_chunk in user_followers:
                graph.add_followers(user_id, follower_chunk, count)
                count += len(follower_chunk)
                print 'Added {} followers'.format(count)
        else:
            print "what"
        # don't conitnue to iterate if this is the source user
        if source_sn:
            break
        else:
            try:
                user_id = graph.get_nodes_missing_rels(rel)[0]
            except:
                print 'No nodes missing relation {}'.format(rel)
                break
