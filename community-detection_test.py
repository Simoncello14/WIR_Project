import json
import datetime
import community
import networkx as nx
import matplotlib.pyplot as plt

#better with karate_graph() as defined in networkx example.
#erdos renyi don't have true community structure



def createGraph(user2partisianship:dict, user2domains:dict, dom2bias:dict) -> nx.Graph:
	graph = nx.Graph() #graph creation - empty graph

	usersSub = list(user2partisianship.items())

	for user, partisianship in usersSub:  #Per il momento non ho considerato la partisianship perché sembra che l'algoritmo della libreria louvain non la utilizzi
		graph.add_node(user)


	for u1,partisianship1 in usersSub:
		for u2,partisianship2 in usersSub:
			if (u1 == u2) or ((u1, u2) in graph.edges): continue

			weight = computeWeight(u1, u2, user2doms, dom2bias)
			if (weight != 0): graph.add_edge(u1, u2, weight= weight) 


	nx.draw(graph)
	#plt.show()

	return graph


def computeWeight(user1, user2, user2doms:dict, dom2bias:dict):
	domainsIntersection = set(user2doms[user1]).intersection(user2doms[user2])
	weight = 0
	
	for domain in domainsIntersection:
		default = 0
		bias = dom2bias.get(domain, default)
		weight += bias

	return weight


def communityDetector(user2partisianship:dict, user2domains:dict, dom2bias:dict):
	G = createGraph(user2partisianship, user2doms, dom2bias)

	#first compute the best partition
	partition = community.best_partition(G)

	#drawing
	size = float(len(set(partition.values())))
	print(partition.values())
	pos = nx.spring_layout(G)
	count = 0.
	for com in set(partition.values()) :
	    count = count + 1.
	    list_nodes = [nodes for nodes in partition.keys()
	                                if partition[nodes] == com]
	    nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
	                                node_color = str(count / size))


	nx.draw_networkx_edges(G, pos, alpha=0.5)
	plt.show()

if __name__ == '__main__':
	print(datetime.datetime.now())
	
	with open('dataset/2k_min_70/2k_min_70/user2doms_70.json', 'r') as users_file:
		user2doms = json.loads(users_file.read())

	with open('dataset/2k_min_70/dom2bias_70.json', 'r') as bias_file:
		dom2bias = json.loads(bias_file.read())

	with open('dataset/2k_min_70/user2partisianship.json', 'r') as partisianship_file:
		user2partisianship = json.loads(partisianship_file.read())

	communityDetector(user2partisianship, user2doms, dom2bias)

	print(datetime.datetime.now())
