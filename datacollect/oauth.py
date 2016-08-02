import datetime
import json
import time
import tweepy
from itertools import cycle

class TwitterAPI(object):

    def __init__(self, json_tokens_path):
        with open(json_tokens_path, 'r') as f:
            self.json_tokens = json.loads(f.read())
        self.apps = cycle(self.json_tokens.keys())
        self.app = self.apps.next()
        self.set_auth()
        self.get_api()

    def set_auth(self):
        tokens = self.json_tokens[self.app]
        self.consumer_key = tokens['consumer_key']
        self.consumer_secret = tokens['consumer_secret']
        self.access_token = tokens['access_token']
        self.access_token_secret = tokens['access_token_secret']

    def get_api(self):
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True,
                              wait_on_rate_limit_notify=True)
        return self.api

    def next_token(self):
        self.app = self.apps.next()
        self.set_auth()
        self.get_api()
        print '/n SWITCHED TO TOKEN {}'.format(self.app)

    def get_user(self, user_id=None, screen_name=None):
        '''Retreives a single user'''
        self.test_rate_limit('users', '/users/show/:id')
        return self.api.get_user(user_id=user_id, screen_name=screen_name)

    def get_users(self, user_ids):
        '''Retrieves users. Reverts to get user'''
        self.test_rate_limit('users', '/users/lookup')
        try:
            users = self.api.lookup_users(user_ids=user_ids)
        except tweepy.TweepError as e:
            print 'Bad user id in batch... getting one-by-one'
            # grab user one-by-one if there is a bad id in the batch
            users = []
            for user_id in user_ids:
                try:
                    user = self.get_user(user_id=user_id)
                except tweepy.TweepError as e:
                    print 'Bad User: ', e.reason
                    user = {'user_id': user_id,
                            'error': e.args[0][0]['message']}
                users.append(user)
        return users

    def get_friends_ids(self, user_id):
    	'''
    	https://dev.twitter.com/docs/api/1.1/get/friends/ids
    	http://docs.tweepy.org/en/latest/api.html#API.friends_ids
    	'''
        self.test_rate_limit('friends', '/friends/ids')
    	for chunk in tweepy.Cursor(self.api.friends_ids,
                                   user_id=user_id, count=5000).pages():
    		yield(chunk)


    def get_followers_ids(self, user_id):
        """Generator returns pages of user ids"""
        self.test_rate_limit('followers', '/followers/ids')
    	for chunk in tweepy.Cursor(self.api.followers_ids,
                                   user_id=user_id, count=5000).pages():
    		yield(chunk)

    def test_rate_limit(self, resources, call_name):
        """
        Tests whether the rate limit of the last request has been reached.
        If it has, cycles to the next token.
        https://dev.twitter.com/rest/reference/get/application/rate_limit_status
        """
        #Get the number of remaining requests
        rls = self.api.rate_limit_status(resources=resources)
        remaining = rls['resources'][resources][call_name]['remaining']
        #Check if we have reached the limit
        if remaining == 1:
            self.next_token()
