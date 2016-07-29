from datacollect import oauth, tgdb

def tgdb_walk(host_port, user, password, json_file, rel, source_sn=None):
    """Valid input for rel is 'FOLLOWING' or 'FOLLOWERS'"""
    graph = tgdb.TwitterGraph(host_port, user, password)
    # connect to twitter API
    tapi = oauth.TwitterAPI(json_file)
    if source_sn:
        user = tapi.get_user(screen_name=source_sn).id # get source user id
    else:
        # get first user node missing relationship
        user = graph.get_nodes_missing_rels(rel)
    # add links for the given user and relationship
    # if there is a source user screen name, only pass once
    # otherwise, will add links for all the users missing relationship
    while user:
        if rel == 'FOLLOWING':
            user_friends = tapi.get_friends_ids(user)
            graph.add_following(user, user_friends)
        elif rel == 'FOLLOWERS':
            print 'waiting on followers'
            user_followers = tapi.get_followers_ids(user)
            print 'adding followers'
            graph.add_followers(user, user_followers)
        else:
            print "what"
        # don't conitnue to iterate if this is the source user
        if source_sn:
            break
        else:
            user = graph.get_nodes_missing_rels(rel)
