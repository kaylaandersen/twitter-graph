import os
from py2neo import Node, Relationship
from py2neo.database import Graph
import oauth

# hook into the graph database
graph = Graph('http://localhost:7474/db/data', user='neo4j',
                 password='IYWcb1ar2')
try:
    graph.schema.create_uniqueness_constraint('User', 'id')
except: #ConstraintViolationException: Constraint already exists
    pass

def add_following(user_id, following_ids):
    user = Node('User', id=user_id)
    graph.merge(user)
    for fid in following_ids:
        user2 = Node('User', id=fid)
        graph.merge(user2)
        graph.merge(Relationship(user, 'FOLLOWS', user2))

def add_user_properties(user_id, cleaned_prop_dict):
    existing_user = Node('User', id=user.id)
    graph.merge(existing_user)
    for k, v in properties_dict.iteritems():
        existing_user[k] = v
    graph.push(existing_user)

def clean_user_dict(user_prop_dict):
    keep = ['contributors_enabled', 'created_at', 'default_profile',
            'default_profile_image', 'description', 'favourites_count',
            'followers_count', 'friends_count', 'geo_enabled', 'id', 'id_str',
            'is_translator', 'lang', 'listed_count', 'location', 'name',
            'profile_image_url_https', 'protected', 'screen_name',
            'statuses_count', 'time_zone', 'utc_offset', 'verified',
            'withheld_in_countries', 'withheld_scope']
    clean = {k: v for k, v in user_prop_dict.iteritems() if k in keys_to_keep}
    image, ext = os.path.split(clean['profile_image_url_https'])
    clean['profile_image_url_https'] = os.path.split(clean['profile_image_url_https']).lstrip('_normal') +






# main
json_file = 'galvanize_capstone1_token.json'
tapi = oauth.TwitterAPI(json_file)
donald = tapi.get_user(screen_name='realDonaldTrump')
hillary = tapi.get_user(screen_name='HillaryClinton')

screen_name = 'realDonaldTrump'
user = tapi.get_user(screen_name=screen_name)
user_friends = tapi.friends_ids(user.id)

add_following(user.id, user_friends)
