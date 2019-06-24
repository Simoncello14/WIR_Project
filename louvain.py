import json
import datetime
import community
import networkx as nx
from networkx.readwrite import json_graph
from random import randint


def createGraph(user2domains:dict, dom2bias:dict) -> nx.Graph:
	graph = nx.Graph() #graph creation - empty graph

	for u1 in user2domains.keys():
		for u2 in user2domains.keys():
			if (u1 == u2) or ((u1, u2) in graph.edges): continue

			weight = computeWeight(u1, u2, user2doms, dom2bias)
			if (weight != 0): graph.add_edge(u1, u2, weight= weight) 

	return graph


def computeWeight(user1, user2, user2doms:dict, dom2bias:dict):
	domainsIntersection = set(user2doms[user1]).intersection(user2doms[user2])
	weight = 0
	
	for domain in domainsIntersection:
		weight += dom2bias.get(domain, 0)

	return weight

def get_k_from(k, user2domains:dict) -> dict:
	new_user2doms = {}
	users = list(user2domains.keys())

	for i in range(k):
		user = users[randint(0, len(users)-1)]
		new_user2doms[user] = user2domains[user]
		users.remove(user)

	return new_user2doms

if __name__ == '__main__':

	print(datetime.datetime.now(), "selecting 5k")
	with open('dataset/295k_min_0/user2doms.json', 'r') as users_file:
		old_user2doms = json.loads(users_file.read())
	user2doms = get_k_from(5000, old_user2doms)
	with open('dataset/20k_from_295k/user2doms_5.json', 'w') as f:
		f.write(json.dumps(user2doms))

	with open('dataset/20k_from_295k/dom2bias.json', 'r') as bias_file:
		dom2bias = json.loads(bias_file.read())

	print(datetime.datetime.now(), "building graph")
	graph = createGraph(user2doms, dom2bias)
	nx.write_weighted_edgelist(graph, 'dataset/20k_from_295k/graph_weighted_edgelist')

	print(datetime.datetime.now(), "using louvain")
	partition = community.best_partition(graph)
	with open('dataset/20k_from_295k/partitions.json', 'w') as part_file:
		part_file.write(json.dumps(partition))

	print(datetime.datetime.now())
