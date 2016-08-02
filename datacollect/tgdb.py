import os
import py2neo
from py2neo import authenticate, Graph, Node, Relationship
from py2neo.database import NodeSelector

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
    def add_following(self, user_id, following_ids, rec_count):
        '''Given a unique user id, adds the relationship for who they follow.
        Adds a User Node with the id if it doesn't exist.'''
        user = Node('User', id=user_id)
        self.graph.merge(user) # important to merge before doing anything
        rec = 1 + rec_count
        # preserving the order of the following. 1 = most recent
        for fid in following_ids:
            user2 = Node('User', id=fid)
            self.graph.merge(user2)
            self.graph.merge(Relationship(user, 'FOLLOWS', user2, rec=rec))
            rec += 1
        user['following_added'] = True
        self.graph.push(user)

    def add_followers(self, user_id, follower_ids, rec_count):
        '''Given a unique user id, adds the relationship for follows them.
        Adds a User Node with the id if it doesn't exist.'''
        user = Node('User', id=user_id)
        self.graph.merge(user)
        rec = 1 + rec_count
        for fid in follower_ids:
            user2 = Node('User', id=fid)
            self.graph.merge(user2)
            self.graph.merge(Relationship(user2, 'FOLLOWS', user, rec=rec))
            rec += 1
        user['followers_added'] = True
        self.graph.push(user)

    def add_user_properties(self, user):
        '''Given a unique user id, adds properties to the existing user Node'''
        try:
            user_id = user.id
            existing_user = Node('User', id=user_id)
            clean_prop_dict = self.__clean_user_dict(user.__dict__)
            self.graph.merge(existing_user)
            for k, v in clean_prop_dict.iteritems():
                existing_user[k] = v
            # add additional label to verified accounts
            if clean_prop_dict['verified']:
                print True
                existing_user.add_label('Verified')
        except:
            # bad user id
            user_id = user['user_id']
            error = user['error']
            existing_user = Node('User', id=user_id)
            self.graph.merge(existing_user)
            existing_user['screen_name'] = 'INVALID'
            existing_user['error'] = error
            print 'Found invalid user id'
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
    def get_nodes_missing_props(self, limit=100):
        '''Returns the first 100 ids of nodes without user properties'''
        selector = NodeSelector(self.graph)
        selected = selector.select('User').where("_.screen_name IS NULL").limit(limit)
        return [s['id'] for s in selected]

    def get_nodes_missing_props_follb(self, limit=100):
        cypherq = """MATCH (n)-[r:FOLLOWS]->(m)
                     WHERE m.screen_name = 'BernieSanders'
                     AND NOT EXISTS(n.screen_name)
                     RETURN n.id
                     LIMIT 100;"""
        return [i['n.id'] for i in self.graph.run(cypherq).data()]

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
        return [s['id'] for s in selected]

    def get_nodes_missing_rels_params(self, rel='FOLLOWING'):
        cypherq = """MATCH (n:User)-[r:FOLLOWS]->(m:User)
                                     WHERE n.followers_count >= 1000
                                     AND NOT EXISTS(n.following_added)
                                     AND m.screen_name = 'BernieSanders'
                                     RETURN n.id
                                     LIMIT 100;"""
        return [i['n.id'] for i in self.graph.run(cypherq).data()]

    def get_nodes_missing_rels_bfriends(self, rel='FOLLOWING'):
        cypherq = """MATCH (n:User)<-[r:FOLLOWS]-(m:User)
                                     WHERE m.screen_name = 'BernieSanders'
                                     AND NOT EXISTS(n.following_added)
                                     RETURN n.id
                                     LIMIT 100;"""
        return [i['n.id'] for i in self.graph.run(cypherq).data()]
