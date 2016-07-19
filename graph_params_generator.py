"""
graph_params_generator.py
Module to generate random graph creation parameters for used in the probing 
algorithm conatined in algorithm.py
"""

import random

def main():

	file = open("paramsG.txt", 'w')
	num_graphs = int(raw_input("How many graphs do you want to create: "))

	i = 0
	while i < num_graphs:
		num_nodes = str(random.randint(30, 200))
		probability = "%.2f" % random.random()
		graph_seed = str(random.randint(1, 150))
		min_edge_weight = str(random.randint(1, 10))
		max_edge_weight = str(random.randint(15, 20))
		weight_seed = str(random.randint(1, 25))

		file.write(str(i) + " " + num_nodes + " " +probability + " " +  graph_seed + " " +
			min_edge_weight + " " + max_edge_weight + " " + weight_seed + "\n")

		i += 1
	file.close()

	new_file = open("paramsC.txt", 'w')
	num_coeffs_sets = int(raw_input("How many sets of coefficients do you want to create: "))

	j = 0
	while j < num_coeffs_sets:
		edge_coverage = "%.2f" % random.uniform(0,1)
		edge_load = "%.2f" % (-random.uniform(0,1))
		node_load = "%.2f" % (-random.uniform(0,1))
		monitoring_s = "%.2f" % random.uniform(0,1)

		new_file.write(edge_coverage + " " + edge_load + " " + node_load + " " + monitoring_s + "\n")

		j += 1
	new_file.close()


if __name__ == "__main__":
	main()
