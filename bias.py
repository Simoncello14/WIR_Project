#!/usr/bin/python3

import json
import datetime


def compute_and_normalize_domains_bias(dom2users:dict, seeds:list) -> dict:
	s_users = []
	for s in seeds:
		s_users.append(set(dom2users[s]))

	max_bias = 0
	dom2bias = {}
	for dom, d_users in dom2users.items():
		if dom in seeds: continue
		bias = 0
		for s in s_users:
			similarity = len(s & set(d_users))
			if similarity>bias: bias = similarity
		dom2bias[dom] = bias
		if bias>max_bias: max_bias=bias

	for dom in dom2bias.keys():
		dom2bias[dom] /= max_bias

	return dom2bias


if __name__ == '__main__':
	print(datetime.datetime.now())
	with open('dataset/seed_domains.json', 'r') as seeds_file:
		seeds = json.loads(seeds_file.read())
	
	with open('dataset/295k_min_0/dom2users.json', 'r') as doms_file:
		dom2users = json.loads(doms_file.read())

	dom2bias = compute_and_normalize_domains_bias(dom2users, seeds)

	with open('dataset/295k_min_0/dom2bias.json', 'w') as bias_file:
		bias_file.write(json.dumps(dom2bias))
	print(datetime.datetime.now())
		