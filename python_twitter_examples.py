#!/usr/bin/python3

import twitter
import json

with open('api_keys.json', 'r') as api_keys_file:
	api_keys = json.loads(api_keys_file.read())

api = twitter.Api(**api_keys)

#print(api.VerifyCredentials())

# https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets
# max is 7 days, count max is 100
# max 450 requests every 15 min
results = api.GetSearch(raw_query="q=car%20&result_type=recent&count=100")
print(len(results))

# https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline.html
# 100k requests/day, 1500 every 15min
# count max is 200, but can be iterated
# this goes beyond 7 days, which is perfect
# timeline = api.GetUserTimeline(screen_name="realDonaldTrump", count=200)
# print(timeline[1])
