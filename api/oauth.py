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
        return self.api.get_user(user_id=user_id, screen_name=screen_name)

    def get_friends(user_id=None, screen_name=None):
        tweepy.Cursor(api.friends)



# main
json_file = 'galvanize_capstone1_token.json'
api = TwitterAPI(json_file)
donald = api.get_user(screen_name='realDonaldTrump')
hillary = api.get_user(screen_name='HillaryClinton')


k = keys['Galvanize Capstone 1']
consumer_key, consumer_secret = k['consumer_key'], k['consumer_secret']
access_token, access_token_secret = k['access_token'],
                                    k['access_token_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

screen_name = 'realDonaldTrump'
api = tweepy.API(auth)

users = tweepy.Cursor(api.followers, screen_name=screen_name).items()
users2 = tweepy.

while True:
    try:
        user = next(users)
    except tweepy.TweepError:
        time.sleep(60*15)
        user = next(users)
    except StopIteration:
        break
    print "@" + user.screen_name
