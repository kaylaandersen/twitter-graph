import os
from py2neo import Node, Relationship
from py2neo.database import Graph, NodeSelector
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
    for k, v in cleaned_prop_dict.iteritems():
        existing_user[k] = v
    if cleaned_prop_dict['verified']:
        existing_user.add_label = 'Verified'
    graph.push(existing_user)

def clean_user_dict(user_prop_dict):

    keep = ['contributors_enabled', 'created_at', 'default_profile',
            'default_profile_image', 'description', 'favourites_count',
            'followers_count', 'friends_count', 'geo_enabled', 'id', 'id_str',
            'is_translator', 'lang', 'listed_count', 'location', 'name',
            'profile_image_url_https', 'protected', 'screen_name',
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

def get_nodes_missing_props(graph):
    selector = NodeSelector(graph)
    selected = selector.select('User').where("_.screen_name IS NULL").limit(100)
    return [s['id'] for s in selected]

# main
json_file = 'galvanize_capstone1_token.json'
tapi = oauth.TwitterAPI(json_file)
bernie = tapi.get_user(screen_name='BernieSanders')
donald = tapi.get_user(screen_name='realDonaldTrump')
hillary = tapi.get_user(screen_name='HillaryClinton')

screen_name = 'realDonaldTrump'
user = tapi.get_user(screen_name=screen_name)
user_friends = tapi.friends_ids(user.id)

add_following(user.id, user_friends)
