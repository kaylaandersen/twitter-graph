import os
import py2neo
from py2neo import authenticate, Graph, Node, Relationship
from py2neo.database import NodeSelector
import oauth

class TwitterGraph(object):
    '''A class for interfacing with the Neo4j Twitter network database'''

    # Initial setup and linking into the database
    def __init__(self, host_port, user, password):
        '''Makes connection to Neo4j database'''
        # set up authentication parameters
        authenticate(host_port, user, password)
        # connect to authenticated graph database
        url = 'http://{}/db/data/'.format(host_port)
        self.graph = Graph(url)
        try:
            self.graph.schema.create_uniqueness_constraint('User', 'id')
        except: #ConstraintViolationException
            print 'Unique id on Node User already exists'

    # Functions to add data to the database
    def add_following(self, user_id, following_ids, source_name, source_degree):
        '''Given a unique user id, adds the relationship for who they follow.
        Adds a User Node with the id if it doesn't exist.'''
        user = Node('User', id=user_id)
        self.graph.merge(user) # important to merge before doing anything
        rec = 1 # preserving the order of the following. 1 = most recent
        for fid in following_ids:
            user2 = Node('User', id=fid)
            user2[source_name] = source_degree
            self.graph.merge(user2)
            self.graph.merge(Relationship(user, 'FOLLOWS', user2, rec=rec))
            rec += 1
        user.following_added = True
        self.graph.push(user)

    def add_followers(self, user_id, follower_ids, source_name, source_degree):
        '''Given a unique user id, adds the relationship for follows them.
        Adds a User Node with the id if it doesn't exist.'''
        user = Node('User', id=user_id)
        self.graph.merge(user)
        rec = 1
        for fid in follower_ids:
            user2 = Node('User', id=fid)
            user2[source_name] = source_degree
            self.graph.merge(user2)
            self.graph.merge(Relationship(user2, 'FOLLOWS', user, rec=rec))
            rec += 1
        user.followers_added = True
        self.graph.push(user)

    def add_user_properties(self, user):
        '''Given a unique user id, adds properties to the existing user Node'''
        existing_user = Node('User', id=user.id)
        clean_prop_dict = self.__clean_user_dict(user.__dict__)
        self.graph.merge(existing_user)
        for k, v in clean_prop_dict.iteritems():
            existing_user[k] = v
        # add additional label to verified accounts
        if clean_prop_dict['verified']:
            print True
            existing_user.add_label('Verified')
        self.graph.push(existing_user)

    def __clean_user_dict(self, user_prop_dict):
        '''Given the '''

        keep = ['contributors_enabled', 'created_at', 'default_profile',
                'default_profile_image', 'description', 'favourites_count',
                'followers_count', 'friends_count', 'geo_enabled', 'id',
                'id_str', 'is_translator', 'lang', 'listed_count', 'location',
                'name', 'profile_image_url_https', 'protected', 'screen_name',
                'statuses_count', 'time_zone', 'utc_offset', 'verified',
                'withheld_in_countries', 'withheld_scope']

        # only keep the above keys for inserting
        clean = {k: v for k, v in user_prop_dict.iteritems() if k in keep}
        image = os.path.splitext(clean['profile_image_url_https'])[0]
        ext = os.path.splitext(clean['profile_image_url_https'])[1]
        clean['profile_image_url_https'] = image.rstrip('_normal') + ext
        # convert date time to string
        clean['created_at_ord'] = clean['created_at'].toordinal()
        clean['created_at'] = clean['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        return clean

    # Functions to query database
    def get_nodes_missing_props(self):
        '''Returns the first 100 ids of nodes without user properties'''
        selector = NodeSelector(self.graph)
        selected = selector.select('User').where("_.screen_name IS NULL").limit(100)
        return [s['id'] for s in selected]

    def get_nodes_missing_rels(self, rel='FOLLOWING', limit=1):
        '''Returns ids missing the follower or following relationships.
        Valid inputs for rel is FOLLOWING or FOLLOWERS'''
        selector = NodeSelector(self.graph)
        if rel == 'FOLLOWING':
            selected = selector.select('User').where("_.following_added IS NULL").limit(limit)
        elif rel == 'FOLLOWERS':
            selected = selector.select('User').where("_.followers_added IS NULL").limit(limit)
        else:
            # TO DO: flesh out the exception calling
            raise Exception

def twitter_graph_walk(graph, tapi, source_sn, depth=3):
    '''Iteratively gets the followers and folllowing users of a source user.
    Depth - how far to grow the graph'''
    source_user = tapi.get_user(screen_name=source_sn)
    for deg in range(1, depth + 1):
        if deg == 1:
            # get user friends
            user_friends = tapi.get_friends_ids(source_user.id)
            # update database
            graph.add_following(source_user.id, user_friends, 'd' + source_sn, deg)
            # get user followers
            user_followers = tapi.get_followers_ids(source_user.id)
            graph.add_followers(source_user.id, user_friends, 'd' + source_sn, deg)

def twitter_graph_fill(graph, tapi):
    '''Hydrate the user node with user data'''
    count = 0 # note this count should be temporary-- need to figure out the api calls
    if count < 150:
        users_to_hyd = graph.get_nodes_missing_props()
        users = tapi.api.lookup_users(user_ids=users_to_hyd)
        for user in users:
            graph.add_user_properties(user)
        count += 1
        print 100 * count





if __name__ == '__main__':
    # connect to network database
    host_port = 'localhost:7474'
    user = 'neo4j'
    password = 'IYWcb1ar2'
    graph = TwitterGraph(host_port, user, password)

    # connect to twitter API
    json_file = 'galvanize_capstone1_token.json'
    tapi = oauth.TwitterAPI(json_file)
    twitter_graph_walk(graph, tapi, 'BernieSanders', depth=1)
    twitter_graph_fill(graph, tapi)
