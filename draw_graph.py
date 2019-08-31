#!/usr/bin/python3

import json
import networkx as nx
import matplotlib.pyplot as plt

print('Loading data')
with open('dataset/5k_from_295k/inv_partitions.json', 'r') as f:
		part2users = json.loads(f.read())

with open('dataset/5k_from_295k/user2doms_5.json', 'r') as f:
		user2doms = json.loads(f.read())

with open('dataset/5k_from_295k/dom2bias.json', 'r') as f:
		dom2bias = json.loads(f.read())

def users_to_weight(a, b):
	result = 0
	a_doms = set(user2doms[a])
	b_doms = set(user2doms[b])
	common = a_doms.intersection(b_doms)
	if len(common)<5: return 0
	for dom in common:
		result += dom2bias.get(dom, 0)
	print(result)
	return result

print('Building graph')
g = nx.Graph()
colors = ['red', 'green', 'blue']
current_color = 0
final_colors = []
final_weights = []

for part in part2users.keys():
	i = 0
	for user in part2users[part]:
		final_colors.append(colors[current_color])
		nodes = g.nodes
		g.add_node(user)
		for n in nodes:
			w = users_to_weight(user, n)
			if w>0:
				g.add_edge(user, n, weight=w)
				final_weights.append(w)
		i +=1
		if i==200: break
	current_color += 1

print("Drawing")
pos = nx.circular_layout(g)
nx.draw(g, pos, node_color=final_colors, width=final_weights, node_size=10)
plt.show()

