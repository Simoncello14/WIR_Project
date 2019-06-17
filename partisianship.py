#!/usr/bin/python3

import json
import datetime
from itertools import combinations

def compute_and_normalize_domains_partisianship(user2domains:dict) -> dict:
	users = [] 

	max_partisianship 	= 0
	user2domscouples 	= {}
	user2partisianship 	= {}

	for user, u_domains in user2domains.items():
		users += user
		#print("DAJE")
		user2domscouples[user] = list(combinations(u_domains, 2)) #takes all possible couples of domains shared by the actual user

	partisianship = 0
	for user in user2domains.keys():
		for userIterator in user2domains.keys():
			if (userIterator != user):
				partisianship += len(set(user2domscouples[user]).intersection(user2domscouples[userIterator]))

		user2partisianship[user] = partisianship
		if (partisianship > max_partisianship): max_partisianship = partisianship
		partisianship = 0 #i have to reset the variable

	for user in user2partisianship.keys():
		user2partisianship[user] /= max_partisianship

	return user2partisianship


if __name__ == '__main__':
	print(datetime.datetime.now())
	
	with open('dataset/35k_min_70/user2doms_70.json', 'r') as users_file:
		user2doms = json.loads(users_file.read())


	user2partisianship = compute_and_normalize_domains_partisianship(user2doms)

	with open('dataset/35k_min_70/user2partisianship.json', 'w') as partisianship_file:
		partisianship_file.write(json.dumps(user2partisianship))
	print(datetime.datetime.now())
		
