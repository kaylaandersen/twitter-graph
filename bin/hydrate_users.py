from datacollect import oauth, tgdb

def twitter_graph_fill(host_port, user, password, json_file):
    # connect to graph database
    graph = tgdb.TwitterGraph(host_port, user, password)
    # connect to twitter API
    tapi = oauth.TwitterAPI(json_file)
    # initiate hydration
    users_to_hyd = graph.get_nodes_missing_props()
    while users_to_hyd:
        users = tapi.get_users(user_ids=users_to_hyd)
        for user in users:
            graph.add_user_properties(user)
        users_to_hyd = graph.get_nodes_missing_props()
    print 'Finished Hydrating Users'

if __name__ == '__main__':
    host_port = 'localhost'
    user = 'neo4j'
    password = 'IYWcb1ar2'
    json_file = 'galvanize_capstone1_token.json'
    twitter_graph_fill(host_port, user, password, json_file)
