import sys
#import matplotlib.pyplot as plt
import networkx as nx 
import random
import csv
import heapqup as hq

def edge_id(edge):
	if (edge[0] > edge[1]):
		return (edge[1], edge[0])
	else: return edge

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


def removeDuplicate(set_of_paths_P):
	'''
	Given a set of paths, remove the duplicated ones 
	[1,2,3] and [3,2,1] are the same. So, one of them is a duplicate
	Input:
		a set of paths (a list of lists)
	Output:
		a set of paths with duplicates removed
	'''
	retListofL = []
	for start_node in set_of_paths_P.keys():
		for end_node in set_of_paths_P[start_node].keys():
			pathL = set_of_paths_P[start_node][end_node]
			if len(pathL) > 1:
				copy_path = pathL[:]
				copy_path.reverse()
				if not (pathL in retListofL or copy_path in retListofL):
					retListofL.append(pathL)
	return retListofL


def get_all_edges_from_SOP(setP):
	'''
	Given a path (list of edges/tuples), get all the edges without duplicates 
	(1,2) and (2,1) are the same. So, one of them is a duplicate
	Input:
		a path (list of edges/tuples)
	Output:
		a path (list of edges/tuples)
	'''
	retL = set()
	for path in setP:
		for i in xrange(len(path)-1):
			temp = edge_id((path[i],path[i+1]))
#			tempRev = (path[i+1], path[i])
#			if not (temp in retL or tempRev in retL):
			retL.add(temp)
	return list(retL)


def scoreFunc(path, uncoveredL):
	'''
	Given a path (list of edges/tuples) and a list of uncovered edges
	if a given path has an "uncovered" edge, increment the score by 1
	Input:
		a path (list of edges/tuples) and a list of uncovered edges
	Output:
		score, which represents how many uncovered edges the input path covers  
	'''
	retScore = 0
	for i in xrange(len(path)-1):
		temp = edge_id((path[i],path[i+1]))
#		tempRev = (path[i+1], path[i])
		bool1 = temp in uncoveredL
#		bool2 = tempRev in uncoveredL
		if  bool1:
			retScore += 1
	return retScore


def deleteEdgesFromL(path, uncoveredL):
	'''
	Given a path (list of edges/tuples) and a list of uncovered edges
	if a given path has an "uncovered" edge, delete the edge in the list of uncovered edges
	Input:
		a path (list of edges/tuples) and a list of uncovered edges
	Output:
		None 
	'''
	for i in xrange(len(path)-1):
		temp = edge_id((path[i],path[i+1]))
#		tempRev = (path[i+1], path[i])
		bool1 = temp in uncoveredL
#		bool2 = tempRev in uncoveredL
		if bool1:
			uncoveredL.remove(temp)
#		if bool2:
#			uncoveredL.remove(tempRev)


def tieBreakerPath(listofPaths, usedMSL):
	'''
	Given a list of paths and a list of used monitoring stations [MS] (nodes)
	Return a path with its endpoints both, one of them or none, being in the list of used MS
	If there are multiple "both"s, return the 1st one (arbitray decision), the same goes for multiple "one"s
	Input:
		list of paths/lists and a list of integers (nodes)
	Output:
		a path/list of integers (nodes)  
	'''
	maxTie = 0
	mTPath = []
	for path in listofPaths:
		if path[0] in usedMSL and path[-1] in usedMSL:
			return path 
		elif path[0] in usedMSL:
			maxTie = 1
			mTPath = path
		elif path[-1] in usedMSL:
			maxTie = 1
			mTPath = path
	
	if maxTie == 0:
		return listofPaths[0]
	return mTPath

def scoreforMS(path, usedMSL):
	if path[0] in usedMSL and path[-1] in usedMSL:
		return 2
	elif path[0] in usedMSL or path[-1] in usedMSL:
		return 1
	else:
		return 0



def greedyAlgorithm(path_dict, uncoveredL, node_loads, edge_loads, coeffs):
	'''
	a Greedy Algorithm that tries to pick, on every iteration, the path with the maximum score 
	Input:
		a set of paths given by the networkx.all_pairs_shortest_paths function
	Output:
		a set of paths picked by Greedy Algorithm
	'''
	#coeficients set to random weight values
	COVERAGE = coeffs[0]
	EDGE_LOAD = coeffs[1]
	NODE_LOAD = coeffs[2]
	MS = coeffs[3]
	
	retPaths = []
	usedMSL = set()

	node_pathL_dict = {}
	edge_pathL_dict = {}
	path_iD_node_load = {}
	path_iD_edge_load = {}

	heap = hq.heapqup(dict(), reverse = True)

	#first loop through all the paths 
	#store their iDs and scores in the max-heap dict
	for path_iD in path_dict.keys():
		path = path_dict[path_iD]
		edge_C_score = scoreFunc(path, uncoveredL)
		edge_L_score = edge_load_score(path, edge_loads)
		node_L_score = node_load_score(path, node_loads)

		path_iD_node_load[path_iD] = node_L_score
		path_iD_edge_load[path_iD] = edge_L_score

		score  = ((COVERAGE * edge_C_score) + (EDGE_LOAD * edge_L_score) + 
					(NODE_LOAD * node_L_score)) #+ MS*scoreforMS(path, usedMSL)
		heap.offer(path_iD, score)
		
		for node in path:
			node_pathL_dict[node] = node_pathL_dict.get(node, [])
			node_pathL_dict[node].append(path_iD)

		for edge in get_all_edges_from_SOP([path]):
			edge_pathL_dict[edge] = edge_pathL_dict.get(edge, [])
			edge_pathL_dict[edge].append(path_iD)

	while len(uncoveredL) > 0: 
		overlapping_paths = set()
		# no need for tie breaking???

		# poll the first path from max-heap
		maxP_iD = heap.poll(True)[0]
		maxP = path_dict[maxP_iD]
		usedMSL.add(maxP[0])
		usedMSL.add(maxP[len(maxP)-1])
		#update load values
		update_load_values(maxP, node_loads, edge_loads)
		# add it to the retPaths
		retPaths.append(maxP)
		# removed edges in this path from uncoveredL
		deleteEdgesFromL(maxP, uncoveredL)
		
		# for all the paths intersecting with it in terms of nodes and edges
		for node in maxP:
			for path_iD in node_pathL_dict[node]:
				path_iD_node_load[path_iD] += 1
				overlapping_paths.add(path_iD)

		for edge in get_all_edges_from_SOP([maxP]):
			for path_iD in edge_pathL_dict[edge]:
				path_iD_edge_load[path_iD] += 1
				overlapping_paths.add(path_iD)
		
		# update their scores (heap.update(path_iD,new_score))
		for path_iD in overlapping_paths:
			path = path_dict[path_iD]
			edge_C_score = scoreFunc(path, uncoveredL)
			edge_L_score = path_iD_edge_load[path_iD]
			node_L_score = path_iD_node_load[path_iD]
			score  = ((COVERAGE * edge_C_score) + (EDGE_LOAD * edge_L_score) + 
					(NODE_LOAD * node_L_score)) + MS*scoreforMS(path, usedMSL)
			heap.update(path_iD, score)
	return retPaths
	

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

	for coeffs in list_of_coeffs:
		iD = 0
		file = open("results3.csv", 'at')
		writer = csv.writer(file)
		writer.writerow(('Coefficients for:', 'Edge Coverage', 'Edge Load', 'Node Load', 'Number of Monitoring Stations'))
		writer.writerow(('', coeffs[0], coeffs[1], coeffs[2], coeffs[3]))

		writer.writerow(('Graph ID', 'Number of Paths Used', 'Total Paths', 'Number of Monitoring Stations', 
			'Average Node Load', 'Maximum Node Load', 'Average Edge Load', 'Maximum Edge Load'))
		for param_graphs in list_of_param_graphs:
			#print "current graph: ", param_graphs
			node_loads = {}
			edge_loads = {}
			paths_used = {}
			H = nx.fast_gnp_random_graph(param_graphs[1], param_graphs[2], param_graphs[3], False)
			randSeed = param_graphs[6]

			for (u,v) in H.edges():
				random.seed(randSeed)
				rInt = random.randint(param_graphs[4], param_graphs[5])
				H[u][v]['w'] = rInt
				randSeed += 1

			#draw_graph(H)
			set_of_paths_P = nx.all_pairs_shortest_path(H)
			setP = removeDuplicate(set_of_paths_P)
			path_dict = create_path_dict(setP)
			uncovered_edges = get_all_edges_from_SOP(setP)

	#		#initilize all network loads
	#		nds = H.nodes()
	#		for nd in nds:
	#			node_loads[nd] = 0
	#		for e in uncovered_edges:
	#			edge_loads[e] = 0

			retPaths = greedyAlgorithm(path_dict, uncovered_edges, node_loads, edge_loads, coeffs)
			print_result(H, retPaths, setP, node_loads, edge_loads, iD, file, writer)
			iD += 1
		file.close()


def node_load_score(path, node_loads):
	"""
	Calculates the node load score of a path
	Input:
		path - the path for which the score is to be calculated
		node_loads - a dictionary holding cumulative loads for each node
	Output:
		score - the node load score of the input path
	"""
	score = 0
	for nd in path:
		score += node_loads.get(nd, 0)

	return score


def edge_load_score(path, edge_loads):
	"""
	Calculates the edge load score of a path
	Input:
		path - the path for which the score is to be calculated
		edge_loads - a dictionary holding cumulative loads for each edge
	Output:
		score - the edge load score of the input path
	"""
	score = 0
	for i in xrange (len(path) - 1):
		edge = edge_id((path[i], path[i + 1]))
#		rev_edge = (path[i + 1], path[i])
        
		score += edge_loads.get(edge, 0)
#        if edge in edge_loads:
 #       	score += edge_loads[edge]
  #  	if rev_edge in edge_loads:
   # 		score += edge_loads[rev_edge]
	return score


def update_load_values(path, node_loads,edge_loads):
	"""
	Given a probing path, updates the node load and edge load dictionaries for each
	node and edge along the path
	Input:
		path - a path picked during an iteration of the greedy algorithm
		node_loads - a dictionary holding cumulative loads for each node
		edge_loads - a dictionary holding cumulative loads for each edge
	"""

	#update node loads
	for nd in path:
		node_loads[nd] = node_loads.get(nd, 0) + 1

	#update edge loads
	for i in range(len(path) - 1):
		edge = edge_id((path[i], path[i + 1]))
#		rev_edge = (path[i + 1], path[i])

		edge_loads[edge] = edge_loads.get(edge, 0) + 1

#		if edge in edge_loads:
#			edge_loads[edge] += 1
#		elif rev_edge in edge_loads:
#			edge_loads[rev_edge] += 1


def print_result(H, output_paths, input_paths, node_loads, edge_loads, iD, file, writer):
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

	#file.write("Paths Used During Probing: " + str(len(output_paths)) + " out of " +
	#	str(len(input_paths)) + "\n")

	numPaths = len(output_paths)
	totalPaths = len(input_paths)
	#for path in output_paths:
	#	file.write(str(path) + "\n")

	#writing Graph iD
	#file.write("Graph ID: " + str(iD))
	#calculate nodes used as monitoring stations
	monitoring_nodes = set()
	for path in output_paths:
		monitoring_nodes.add(path[0])
		monitoring_nodes.add(path[len(path)-1])

	#file.write("\nNodes Used as Monitoring Station: \n" + str(monitoring_nodes) + "\n" + 
	#	"Number of Monitoring Stations: " + str(len(monitoring_nodes)) + "\n")
	#file.write("\n\nNumber of Monitoring Stations: " + str(len(monitoring_nodes)) + "\n")
	numMS = len(monitoring_nodes)
	#calculate node load results
	total_load = 0
	max_load = 0
	max_load_index = 0

	for nd in node_loads:
		load = node_loads[nd]
		total_load += load

		if load > max_load:
			max_load = load
			max_load_index = nd

	mean_load = float(total_load)/nx.number_of_nodes(H)

	avg_Node_Load = mean_load
	max_Node_Load = max_load

	#file.write("\n-----------------\nNode Loads\n" +
	#	"- Average Node Load: " + str(mean_load) +
	#	"\n- Maximum Node Load: " + str(max_load) + " on node " + str(max_load_index))
	#file.write("\n All Node Loads: \n" + str(node_loads)+"\n")

	#calculate edge load results
	total_load = 0
	max_load = 0
	max_load_index = 0

	for eg in edge_loads:
		load = edge_loads[eg]
		total_load += edge_loads[eg]

		if load > max_load:
			max_load = load
			max_load_index = eg

	mean_load = float(total_load) / nx.number_of_edges(H)
	
	avg_Edge_Load = mean_load
	max_Edge_Load = max_load
	'''
	file.write("\n-----------------\nEdge Loads\n" +
		"- Average Edge Load: " + str(mean_load) +
		"\n- Maximum Edge Load: " + str(max_load) + " on edge " + str(max_load_index))
	
	
	file.write("\n All Edge Loads: \n")
	i = 0
	while i < len(edge_loads.keys()) - 4:
		edge0 = edge_loads.keys()[i]
		edge1 = edge_loads.keys()[i+1]
		edge2 = edge_loads.keys()[i+2]
		edge3 = edge_loads.keys()[i+3]

		load_on_edge0 = edge_loads[edge0]
		load_on_edge1 = edge_loads[edge1]
		load_on_edge2 = edge_loads[edge2]
		load_on_edge3 = edge_loads[edge3]

		formatted_str = (str(edge0) + " : " + str(load_on_edge0) + " | " +
			str(edge1) + " : " + str(load_on_edge1) + " | " + 
			str(edge2) + " : " + str(load_on_edge2) + " | " +
			str(edge3) + " : " + str(load_on_edge3) + "\n") 
		file.write(formatted_str)
		i += 4 
	'''
	#file.write("\n--------------------------------------------------------------\n")
	writer.writerow((iD, numPaths, totalPaths, numMS, "%.2f" % avg_Node_Load, max_Node_Load,
		"%.2f" % avg_Edge_Load, max_Edge_Load))
	#file.close()


if __name__ == "__main__":
	# argv[1] - file for list of graph parameters
	# argv[2] - file for list of coefficients
    main([sys.argv[1], sys.argv[2]])












