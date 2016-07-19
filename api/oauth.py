import json
import tweepy

with open('galvanize_capstone1_token.json', 'r') as f:
    keys = json.loads(f.read())
consumer_key, consumer_secret = keys['consumer_key'], keys['consumer_secret']
access_token, access_token_secret = keys['access_token'], keys['access_token_secret']

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
