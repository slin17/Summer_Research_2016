import sys
#import matplotlib.pyplot as plt
import networkx as nx 
import greedy_framework as gf
import graph_cleanup as gc
import random
import csv

'''
def draw_graph(H):
	
	a function to draw a given graph with nodes labelled
	Input:
		H - a graph created by networkx.fast_gnp_random_graph() method
	Output:
		None
	
	labelsdict = {}
	for node in H.nodes():
		labelsdict[node] = str(node)
	pos=nx.spring_layout(H)
	nx.draw(H, labels = labelsdict, with_label = True)
	plt.show()
'''

def read_graphs_params(filename):
	"""
	Reads a series of graph generation parameters from a file
	Input:
		filename - the nam of the file to be read from
	Output:
		list_of_param_graphs - a list of graph generation parameters
	"""
	list_of_param_graphs = []
	file = open(filename, "r")
	list_of_lines = file.readlines()
	for raw_line in list_of_lines:
		param_graphs = []
		line = raw_line.strip().split()
		for i in xrange(len(line)):
			if i == 2:
				param_graphs.append(float(line[i]))
			else:
				param_graphs.append(int(line[i]))
		list_of_param_graphs.append(param_graphs)

	return list_of_param_graphs


def read_coeff(filename):
	list_of_coeffs = []
	file = open(filename, "r")
	list_of_lines = file.readlines()
	for raw_line in list_of_lines:
		coeffs = []
		line = raw_line.strip().split()
		for item in line:
			coeffs.append(float(item))
		list_of_coeffs.append(coeffs)
	return list_of_coeffs

def create_path_dict(setP):
	i = 0
	ret_dict = {}
	for path in setP:
		ret_dict[str(i)] = path
		i += 1
	return ret_dict

def main(list_of_filenames):
	"""
	Starting point of the program. Creates a series of graphs and for each runs the 
	probing algorithm, writing the results to a file
	Input:
		filename - name of the file from which to read graph generation parameters
	"""

	#read graph creation properties from file
	list_of_param_graphs = read_graphs_params(list_of_filenames[0])
	list_of_coeffs = read_coeff(list_of_filenames[1])

	list_of_setP = []
	list_of_path_dict = []
	list_of_uncovered_edges = []

	for param_graphs in list_of_param_graphs:
			H = nx.fast_gnp_random_graph(param_graphs[1], param_graphs[2], param_graphs[3], False)
			randSeed = param_graphs[6]

			for (u,v) in H.edges():
				random.seed(randSeed)
				rInt = random.randint(param_graphs[4], param_graphs[5])
				H[u][v]['w'] = rInt
				randSeed += 1

			set_of_paths_P = nx.all_pairs_shortest_path(H)
			setP = gc.remove_duplicate_paths(set_of_paths_P)
			list_of_setP.append(setP)
			path_dict = create_path_dict(setP)
			list_of_path_dict.append(path_dict)
			uncovered_edges = gc.get_all_edges_from_SOP(setP)
			list_of_uncovered_edges.append(uncovered_edges)

	file = open("re.csv", 'at')
	writer = csv.writer(file)

	iD = 0
	for idx in xrange(len(list_of_setP)): #loop through the graphs

		writer.writerow(('Graph ID', 'Coefficients',  'Number of Paths Used', 'Total Paths', 'Number of Monitoring Stations', 
				'Average Node Load', 'Maximum Node Load', 'Average Edge Load', 'Maximum Edge Load'))

		for coeffs in list_of_coeffs:
			t_path_dict = list_of_path_dict[idx]
			t_uncovered_edges = set(list_of_uncovered_edges[idx])
			t_setP = list_of_setP[idx]
			x,y = bs_OC.b_s_1(0, 5, idx, list_of_uncovered_edges, gf.func_wrapper_greedy_algo, t_path_dict, coeffs)
			print "start_coeff: %.2f, end_coeff: %.2f" %(x,y)
			opt_c = bs_OC.b_s_2(x, y, 5, idx, list_of_uncovered_edges, gf.func_wrapper_greedy_algo, t_path_dict, coeffs)
			print "opt_coeff: %.2f" %(opt_c)
			#sev_tuple = func_wrapper_greedy_algo(t_path_dict, t_uncovered_edges, coeffs, t_path_dict)
			#print_result(file, iD, coeffs, sev_tuple[0], len(t_setP), sev_tuple[1], sev_tuple[2], sev_tuple[3], sev_tuple[4], sev_tuple[5])
		iD += 1

	file.close()

def print_result(file, iD, coeffs, numPaths, totalPaths, numMS, avg_Node_Load, max_Node_Load, avg_Edge_Load, max_Edge_Load):
	"""
	Given a list of paths returned by the greedy algorithm, evaluates the maximum and avarage edge and
	node metrics and writes these to a file
	Input:
		H - the graph
		retPaths - a list of paths returned by the greedy algorithm
		inPaths - a list of paths supplied as input to the greedy algorith calculated
				  form networkx.all_pair_shortest_paths()
		node_loads - a dictionary holding cumulative loads for each node
		edge_loads - a dictionary holding cumulative loads for each edge
	Output:
		apppeds data to a file, results.txt
	"""
	coeff = ""
	for c in coeffs:
		coeff += str(c) + " "
	writer.writerow((iD, coeff, numPaths, totalPaths, numMS, "%.2f" % avg_Node_Load, max_Node_Load,
		"%.2f" % avg_Edge_Load, max_Edge_Load))


if __name__ == "__main__":
	# argv[1] - file for list of graph parameters
	# argv[2] - file for list of coefficients
    main([sys.argv[1], sys.argv[2]])












