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
        self.api = tweepy.API(self.auth)
        return self.api

    def next_token(self):
        self.app = self.apps.next()
        self.set_auth()
        self.get_api()

    def get_user(self, user_id=None, screen_name=None):
        '''Retreives a single user'''
        return self.api.get_user(user_id=user_id, screen_name=screen_name)

    def get_users(self):
        pass

    def get_friends(self, user_id=None, screen_name=None):
        ids = []
        cursor = api.api.friends_ids(user_id=user_id,
                                      screen_name=screen_name,
                                      cursor=-1)
        return cursor

    def friends_ids(self, user_id):
    	"""
    	https://dev.twitter.com/docs/api/1.1/get/friends/ids
    	http://docs.tweepy.org/en/latest/api.html#API.friends_ids
    	"""
        friend_ids = []
    	for chunk in tweepy.Cursor(self.api.friends_ids,
                                   user_id=user_id, count=5000).pages():
    		friend_ids.extend(chunk)
        return friend_ids
