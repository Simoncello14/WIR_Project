#!/usr/bin/python3

import tweepy
import json
import datetime
import os
from urllib.parse import urlparse

def create_api(api_keys):
	auth = tweepy.OAuthHandler(api_keys["consumer_key"], api_keys["consumer_secret"])
	auth.set_access_token(api_keys["access_token_key"], api_keys["access_token_secret"])
	return tweepy.API(auth, wait_on_rate_limit=True)

def crawl_users(api, seed_domains: list):
	for domain in seed_domains:
		if os.path.isfile(domain+'_temp.txt'):
			print("[{}][crawl_users]: skipping '{}'".format(dt_now(), domain))
			continue
		print("[{}][crawl_users]: using '{}'".format(dt_now(), domain))
		dom_users = set()
		# I write intermediate result both to check for progress and prevent loss of data
		with open(domain+'_temp.txt', 'w') as out_users_file:
			tweets = True
			last_id = None
			while tweets:
				tweets = api.search(q=domain, tweet_mode="extended", count=100, include_entities="false", max_id=last_id)
				for t in tweets:
					screen_name = t._json["user"]["screen_name"]
					dom_users.add(screen_name)
					out_users_file.write(screen_name+'\n') # will contain duplicates
					last_id = t._json["id"]-1
		with open('domain2users/'+domain+'_set.txt', 'w') as out_dom_file:
			users_to_json_array = json.dumps(list(dom_users))
			out_dom_file.write(users_to_json_array)

# output: {"screen_name":[domain_1, domain_2]}
def crawl_domains(api, users: list):
	n_user = len(users)
	i = 0
	for user in users:
		i+=1
		if os.path.isfile('user2domains/'+user+'.json'):
			print("[{}][crawl_domains][{}/{}]: skipping user '{}'".format(dt_now(), i, n_user, user))
			continue
		print("[{}][crawl_domains][{}/{}]: crawling from user '{}'".format(dt_now(), i, n_user, user))

		user_doms = set()

		# I only take the last 200
		tweets = api.user_timeline(screen_name=user, count=200, tweet_mode="extended")
		for t in tweets:
			for url in t._json["entities"]["urls"]:
				domain = urlparse(url["expanded_url"]).netloc
				user_doms.add(domain)
		print("[{}][crawl_domains]: got {} domains".format(dt_now(), len(user_doms)))

		with open('user2domains/'+user+'.json', 'w') as user_doms_file:
			user_doms_file.write(json.dumps(list(user_doms)))





if __name__ == '__main__':
	dt_now = datetime.datetime.now
	# with open('seed_domains.json', 'r') as seed_domains_file:
	# 	seed_domains = json.loads(seed_domains_file.read())

	with open('api_keys.json', 'r') as api_keys_file:
		api_keys = json.loads(api_keys_file.read())

	print("[{}] Autheticating...".format(dt_now()))
	api = create_api(api_keys)
	print("Autheticated: ", api.me().name)

	# print("[{}] Crawling users...".format(dt_now()))
	# users = crawl_users(api, seed_domains)
	# print("[{}] Got {} users...".format(dt_now(), len(users)))

	with open('users.json', 'r') as users_file:
		users = json.loads(users_file.read())

	print("[{}] Crawling domains...".format(dt_now()))
	crawl_domains(api, users)
