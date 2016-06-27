import sys
import matplotlib.pyplot as plt
import networkx as nx 
import random


def draw_graph(H):
	'''
	a function to draw a given graph with nodes labelled
	Input:
		H - a graph created by networkx.fast_gnp_random_graph() method
	Output:
		None
	'''
	labelsdict = {}
	for node in H.nodes():
		labelsdict[node] = str(node)
	pos=nx.spring_layout(H)
	nx.draw(H, labels = labelsdict, with_label = True)
	plt.show()


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
	retL = []
	for path in setP:
		for i in xrange(len(path)-1):
			temp = (path[i],path[i+1])
			tempRev = (path[i+1], path[i])
			if not (temp in retL or tempRev in retL):
				retL.append(temp)
	return retL


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
		temp = (path[i],path[i+1])
		tempRev = (path[i+1], path[i])
		bool1 = temp in uncoveredL
		bool2 = tempRev in uncoveredL
		if  bool1 or bool2:
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
		temp = (path[i],path[i+1])
		tempRev = (path[i+1], path[i])
		bool1 = temp in uncoveredL
		bool2 = tempRev in uncoveredL
		if bool1:
			uncoveredL.remove(temp)
		if bool2:
			uncoveredL.remove(tempRev)


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


def greedyAlgorithm(setP, uncoveredL, node_loads, edge_loads):
	'''
	a Greedy Algorithm that tries to pick, on every iteration, the path with the maximum score 
	Input:
		a set of paths given by the networkx.all_pairs_shortest_paths function
	Output:
		a set of paths picked by Greedy Algorithm
	'''
	#coeficients set to random weight values
	COVERAGE = 0.5
	EDGE_LOAD = 0.25
	NODE_LOAD = 0.25
	
	retPaths = []
	usedMSL = set()
	hSDict = {}
	maxP = []
	while len(uncoveredL) > 0:
		maxScore = -1
		
		for path in setP:
			score = scoreFunc(path, uncoveredL)

			if score > 0:
				score  = ((COVERAGE * score) + (EDGE_LOAD * edge_load_score(path, edge_loads)) + 
					(NODE_LOAD * node_load_score(path, node_loads)))
			else:
				continue

			if score > maxScore:
				hSDict.clear()
				hSDict[score] = [path]
				maxScore = score

			if score == maxScore:
				#store all paths this a score == highscore
				if path not in hSDict[score]:
					hSDict[score].append(path)

		lP = hSDict[hSDict.keys()[0]]	#list of tied paths
		if len(lP) > 1:
			maxP = tieBreakerPath(lP, usedMSL)
		else:
			maxP = lP[0]

		deleteEdgesFromL(maxP, uncoveredL)
		retPaths.append(maxP)

		#keep track of nodes used as monitoring stations
		usedMSL.add(maxP[0])
		usedMSL.add(maxP[-1])
		setP.remove(maxP)

		#update load values
		update_load_values(maxP, node_loads, edge_loads)
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
			if i == 1:
				param_graphs.append(float(line[i]))
			else:
				param_graphs.append(int(line[i]))
		list_of_param_graphs.append(param_graphs)

	return list_of_param_graphs


def main(filename):
	"""
	Starting point of the program. Creates a series of graphs and for each runs the 
	probing algorithm, writing the results to a file
	Input:
		filename - name of the file from which to read graph generation parameters
	"""
	#read graph creation properties from file
	list_of_param_graphs = read_graphs_params(filename)

	for param_graphs in list_of_param_graphs:
		#print "current graph: " + str(param_graphs)
		node_loads = {}
		edge_loads = {}
		paths_used = {}
		H = nx.fast_gnp_random_graph(param_graphs[0], param_graphs[1], param_graphs[2], False)
		randSeed = param_graphs[5]

		for (u,v) in H.edges():
			random.seed(randSeed)
			rInt = random.randint(param_graphs[3], param_graphs[4])
			H[u][v]['w'] = rInt
			randSeed += 1

		draw_graph(H)
		set_of_paths_P = nx.all_pairs_shortest_path(H)
		setP = removeDuplicate(set_of_paths_P)
		uncovered_edges = get_all_edges_from_SOP(setP)

		#initilize all network loads
		nds = H.nodes()
		for nd in nds:
			node_loads[nd] = 0
		for e in uncovered_edges:
			edge_loads[e] = 0

		retPaths = greedyAlgorithm(setP, uncovered_edges, node_loads, edge_loads)
		print_result(retPaths, setP, node_loads, edge_loads)


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
		score += node_loads[nd]

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
	for i in range (len(path) - 1):
		edge = (path[i], path[i + 1])
		rev_edge = (path[i + 1], path[i])
        
        if edge in edge_loads:
        	score += edge_loads[edge]
    	elif rev_edge in edge_loads:
    		score += edge_loads[rev_edge]
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
		node_loads[nd] += 1

	#update edge loads
	for i in range(len(path) - 1):
		edge = (path[i], path[i + 1])
		rev_edge = (path[i + 1], path[i])

		if edge in edge_loads:
			edge_loads[edge] += 1
		elif rev_edge in edge_loads:
			edge_loads[rev_edge] += 1


def print_result(output_paths, input_paths, node_loads, edge_loads):
	"""
	Given a list of paths returned by the greedy algorithm, evaluates the maximum and avarage edge and
	node metrics and writes these to a file
	Input:
		retPaths - a list of paths returned by the greedy algorithm
		inPaths - a list of paths supplied as input to the greedy algorith calculated
				  form networkx.all_pair_shortest_paths()
		node_loads - a dictionary holding cumulative loads for each node
		edge_loads - a dictionary holding cumulative loads for each edge
	Output:
		apppeds data to a file, results.txt
	"""

	file = open("results.txt", 'a')
	
	file.write("Paths Used During Probing: " + str(len(output_paths)) + " out of " +
		str(len(input_paths)) + "\n")

	for path in output_paths:
		file.write(str(path) + "\n")

	#calculate nodes used as monitoring stations
	monitoring_nodes = set()
	for path in output_paths:
		monitoring_nodes.add(path[0])
		monitoring_nodes.add(path[len(path)-1])

	file.write("\nNodes Used as Monitoring Station: \n" + str(monitoring_nodes) + "\n")

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

	mean_load = total_load/len(node_loads.keys())

	file.write("\n-----------------\nNode Loads\n" +
		"- Average Node Load: " + str(mean_load) +
		"\n- Maximum Node Load: " + str(max_load) + " on node " + str(max_load_index))
	file.write("\n All Node Loads: \n" + str(node_loads)+"\n")

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

	mean_load = total_load / len(edge_loads.keys())

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
	file.write("\n--------------------------------------------------------------\n")
	file.close()


if __name__ == "__main__":
    main(sys.argv[1])












