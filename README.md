##Flock
###Overview
I created a graph representation of the twitter network surrounding Bernie Sanders.

###Data Collection
Data was collected from the Twitter REST API using the tweepy module to collect data from three endpoints:

  1. GET friends/ids: returns pages of user ids the queries user is following
  2. GET followers/ids: returns pages of user ids that are following the queried user.
  3. GET users/lookup: returns the properties of the queried user, used to hydrate the user nodes with properties more than just their Twitter ID.

The Twitter API is rate-limited, which limits the amount of data we can collect in a given time period.

###Data Storage
Users were stored as nodes in a Neo4j database structure. The properties loaded onto each user node include friends/follower counts, if verified, if geotagging is enabled, location, profile picture, etc. See https://dev.twitter.com/overview/api/users for full property list.

Follower and following links between users were are stored as relationship objects between nodes. The properties loaded onto the relationships are direction and an ordinal value indicating the order the following relationship began.

###Next Steps
In order for effective graphing analysis of pivotal users and neighborhood clustering, another data collection step is needed to add weight to the relationships between users. To do this, an additional API listener on the users in the network will be opened up to catch information such as retweets, favorites, and replies.
