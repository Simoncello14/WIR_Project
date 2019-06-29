#!/usr/bin/python3

import json
import os
import sys

def build_inverted_index(dir_path):
	user2doms = {}
	num2users = {} #how many users have k domains?
	dom2user = {}
	i = 0
	for entry in os.scandir(dir_path):
		i+=1
		print(i)
		if entry.name == '.keep': continue
		with open(dir_path+entry.name, 'r') as entry_file:
			try:
				user_doms = json.loads(entry_file.read())
			except:
				print('skipped')

		dom_len = len(user_doms)
		screen_name = entry.name.split('.')[0]
		num2users[dom_len] = num2users.get(dom_len, 0)+1
		user2doms[screen_name] = user_doms
		for dom in user_doms:
			dom2user[dom] = dom2user.get(dom, [])+[screen_name]

	with open('user2doms.json', 'w') as f:
		f.write(json.dumps(user2doms))

	with open('num2users.json', 'w') as f:
		f.write(json.dumps(num2users))

	with open('dom2users.json', 'w') as f:
		f.write(json.dumps(dom2user))

def avg_dom_per_user():
	with open('num2users.json', 'r') as f:
		num2users = json.loads(f.read())
	avg_dom_per_user = 0
	for num, users in num2users.items():
		avg_dom_per_user += int(num)*users
	avg_dom_per_user /= 295311
	print("Avg num of doms per user: ", avg_dom_per_user)

def num_of_users_with_more_than(min_doc):
	with open('num2users.json', 'r') as f:
		num2users = json.loads(f.read())
	out = 0
	for num, users in num2users.items():
		if num > min_doc: out += users
	print(out)

def create_json_with_users_with_more_than(min_doc):
	new_user2doms = {}
	new_dom2users = {}

	with open('user2doms.json', 'r') as f:
		user2doms = json.loads(f.read())

	for user, doms in user2doms.items():
		if len(doms)>min_doc:
			new_user2doms[user] = doms
			for d in doms:
				new_dom2users[d] = new_dom2users.get(d, [])+[user]

	with open('user2doms_'+str(min_doc)+'.json', 'w') as f:
		f.write(json.dumps(new_user2doms))

	with open('dom2users_'+str(min_doc)+'.json', 'w') as f:
		f.write(json.dumps(new_dom2users))


create_json_with_users_with_more_than(int(sys.argv[1]))
