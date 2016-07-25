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
            graph.schema.create_uniqueness_constraint('User', 'id')
        except py2neo.ConstraintError:
            print 'Unique id on Node User already exists'

    # Functions to add data to the database
    def add_following(self, user_id, following_ids):
        '''Given a unique user id, adds the relationship for who they follow.
        Adds a User Node with the id if it doesn't exist.'''
        user = Node('User', id=user_id)
        self.graph.merge(user) # important to merge before doing anything
        for fid in following_ids:
            user2 = Node('User', id=fid)
            self.graph.merge(user2)
            self.graph.merge(Relationship(user, 'FOLLOWS', user2))

    def add_followers(self, user_id, follower_ids):
        '''Given a unique user id, adds the relationship for follows them.
        Adds a User Node with the id if it doesn't exist.'''
        user = Node('User', id=user_id)
        self.graph.merge(user)
        for fid in follower_ids:
            user2 = Node('User', id=fid)
            self.graph.merge(user2)
            self.graph.merge(Relationship(user2, 'FOLLOWS', user))

    def add_user_properties(self, user_id, user_prop_dict):
        '''Given a unique user id, adds properties to the existing user Node'''
        existing_user = Node('User', id=user.id)
        clean_prop_dict = self.__clean_user_dict(user_prop_dict)
        self.graph.merge(existing_user)
        for k, v in clean_prop_dict.iteritems():
            existing_user[k] = v
        # add additional label to verified accounts
        if clean_prop_dict['verified']:
            existing_user.add_label = 'Verified'
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
    def get_nodes_missing_props(graph):
        '''Returns the first 100 ids of nodes without user properties'''
        selector = NodeSelector(graph)
        selected = selector.select('User').where("_.screen_name IS NULL").limit(100)
        return [s['id'] for s in selected]

if __name__ == '__main__':
    # connect to network database
    host_port = 'localhost:7474'
    user = 'neo4j'
    password = 'IYWcb1ar2'
    graph = TwitterGraph(host_port, user, password)

    json_file = 'galvanize_capstone1_token.json'
    tapi = oauth.TwitterAPI(json_file)
    bernie = tapi.get_user(screen_name='BernieSanders')

    screen_name = 'realDonaldTrump'
    user = tapi.get_user(screen_name=screen_name)
    user_friends = tapi.friends_ids(user.id)

    add_following(user.id, user_friends)

    # SUDO CODE
    # Get
