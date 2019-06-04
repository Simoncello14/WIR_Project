#!/usr/bin/python3

import tweepy
import json

with open('api_keys.json', 'r') as api_keys_file:
	api_keys = json.loads(api_keys_file.read())

auth = tweepy.OAuthHandler(api_keys["consumer_key"], api_keys["consumer_secret"])
auth.set_access_token(api_keys["access_token_key"], api_keys["access_token_secret"])

api = tweepy.API(auth)

# search = api.search('polpetta', rpp=100, result_type="recent", tweet_mode="extended", count=200)
# print(len(search))
# # print(search[1])

tweets = api.user_timeline(screen_name="DeBortoliF",count=200, tweet_mode="extended")
print(len(tweets))
# print(json.dumps(tweets[1]._json, indent=4))
# print("\n\n\n")
# print(json.dumps(tweets[2]._json, indent=4))
# print("\n\n\n")
# print(json.dumps(tweets[3]._json, indent=4))