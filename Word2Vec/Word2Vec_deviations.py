#!/usr/bin/python3

from gensim.utils import simple_preprocess
from gensim.models import Word2Vec, KeyedVectors
import os
import sys
import json
import datetime
import numpy as np



def preprocess_tweets2tokens(dir_path):
	partition_ds = [] # It is a list of lists, each element corresponds to a tweet
	i = 1
	for entry in os.scandir(dir_path):
		print(i)
		i += 1
		if entry.name == '.keep': continue
		with open(dir_path+entry.name, 'r') as f:
			try:
				user_tweets = json.loads(f.read())
				for t in user_tweets:
					partition_ds.append(simple_preprocess(t))
			except:
				print('skipped')  
	with open(dir_path+'w2v_perc.json', 'w') as out:
		out.write(json.dumps(partition_ds))

def train_W2V_model(dataset, name):
	model = Word2Vec(
		dataset,
		size=100,
		window=10,
		min_count=2,
		workers=10,
		iter=10)

	model.save(name+".model")

def compute_deviations(global_wv, partition_vw):
	deviations = [] # list of tuples, ("word", deviation)
	i = 0
	for t in partition_vw.vocab.keys():
		i += 1
		print(i)
		try:
			dev = cosine_distance(global_wv[t], partition_vw[t])
			deviations.append((t, dev))
		except:
			print('Exception on:', t)
	return deviations
			

def cosine_distance(v1, v2): # [0, 1]
  dot = np.dot(v1, v2)
  norm1 = np.linalg.norm(v1)
  norm2 = np.linalg.norm(v2)
  cos_sim = ((dot/(norm1*norm2))+1)/2
  return (1-cos_sim)

if __name__ == '__main__':
	print(datetime.datetime.now())

	#preprocess_tweets2tokens(sys.argv[1])
	
	# with open(sys.argv[1], 'r') as f:
	# 	dataset = json.loads(f.read())
	# train_W2V_model(dataset, sys.argv[2])

	p = Word2Vec.load("partition_1.model").wv
	g = KeyedVectors.load_word2vec_format("Set3_TweetDataWithSpam_Word.bin", binary=True)
	devs = compute_deviations(g, p)
	with open('deviations_1.json', 'w') as f:
		f.write(json.dumps(devs))

	print(datetime.datetime.now())