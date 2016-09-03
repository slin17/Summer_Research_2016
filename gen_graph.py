"""
gen_graph.py
Module to generate random graph creation parameters for used in the probing 
algorithm
"""

import random
import os
import sys

def main(file_to_open):
	"""
	Given the name of a file, generates random graph generation arguments and writes 
	then to the file.
	"""

	graph_type = {0: (10,60), 1: (60, 200),  2: (0.005, 0.1), 3: (0.1, 0.25)}
	# 0 - small, 1 - large
	# 2 - sparse, 3 - dense
	
	f = open(os.path.expanduser("./gnc/"+file_to_open), 'a')
	
	type_graphs = raw_input("ss - small, sparse, sd - small, dense, ls - large, sparse, ld - large, dense: ").strip()
	num_graphs = int(raw_input("How many graphs?: "))

	t_g_dict = {'ss': [graph_type[0],graph_type[2]], 'sd': [graph_type[0],graph_type[3]], 
					'ls': [graph_type[1],graph_type[2]], 'ld': [graph_type[1],graph_type[3]]}
	n_range = t_g_dict[type_graphs][0]
	e_prob = t_g_dict[type_graphs][1]

	for i in xrange(num_graphs):
		num_nodes = str(random.randint(n_range[0], n_range[1]))
		probability = "%.3f" % random.uniform(e_prob[0], e_prob[1])
		graph_seed = str(random.randint(1, 150))
		min_edge_weight = str(random.randint(1, 5))
		max_edge_weight = str(random.randint(5, 15))
		weight_seed = str(random.randint(1, 25))

		f.write(''.join([str(i), " ", num_nodes, " ", probability, " ", graph_seed, " ",
			min_edge_weight, " ", max_edge_weight, " ", weight_seed, "\n"]))
	f.close()

if __name__ == "__main__":
	main(sys.argv[1])
