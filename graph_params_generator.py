"""
graph_params_generator.py
Module to generate random graph cration parameters for used in the probing 
algorithm conatined in algorithm.py
"""

import random

def main():

	file = open("test_graph_params.txt", 'a')
	num_graphs = int(raw_input("How many graphs do you want to create: "))

	i = 0
	while i < num_graphs:
		num_nodes = random.randint(10, 100)
		probability = "%.2f" % random.random()
		graph_seed = random.randint(1, 999)
		min_edge_weight = random.randint(1, 5)
		max_edge_weight = random.randint(5, 10)
		weight_seed = random.randint(1, 100)

		file.write(num_nodes, probability, graph_seed,
			min_edge_weight, max_edge_weight, weight_seed)

		i++



if __name__ == "__main__":
	main()
