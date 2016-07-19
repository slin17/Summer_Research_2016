import heapqup as hq
import binary_search_OC as bs_OC
import compu_score as cos
import graph_cleanup as gc

def greedy_algorithm(path_dict, set_uncovered_edges, node_loads, edge_loads, coeffs):
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
	
	ret_path_iDs = set()
	used_MS_set = set()

	node_pathL_dict = {}
	edge_pathL_dict = {}
	path_iD_node_load = {}
	path_iD_edge_load = {}
	path_iD_edge_coverage = {}
	path_iD_MS_score = {}

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
		path_iD_edge_coverage[path_iD] = edge_C_score

		score  = ((COVERAGE * edge_C_score) + (EDGE_LOAD * edge_L_score) + 
					(NODE_LOAD * node_L_score)) #+ MS*scoreforMS(path, usedMSL)
		heap.offer(path_iD, score)
		
		for node in path:
			node_pathL_dict[node] = node_pathL_dict.get(node, set())
			node_pathL_dict[node].add(path_iD)

		for edge in get_all_edges_from_SOP([path]):
			edge_pathL_dict[edge] = edge_pathL_dict.get(edge, set())
			edge_pathL_dict[edge].add(path_iD)

	while len(set_uncovered_edges) > 0: 
		overlapping_paths = set()
		# peek all the paths with the max score from max-heap
		maxP_iD_list = heap.peek_all()
		# randomly break ties
		maxP_iD = cos.random_tie_breaker(maxP_iD_list)
		# remove that path from heap
		heap.remove(maxP_iD)
		maxP = path_dict[maxP_iD]
		used_MS_set.add(maxP[0])
		used_MS_set.add(maxP[len(maxP)-1])
		#update load values
		update_load_values(maxP, node_loads, edge_loads)
		# add it to the retPaths
		ret_path_iDs.add(maxP_iD)
		# removed edges in this path from uncoveredL
		newly_covered_edges = gc.delete_edges_from_s(maxP, set_uncovered_edges)
		
		# for all the paths intersecting with it in terms of nodes and edges
		for node in maxP:
			for path_iD in node_pathL_dict[node]:
				if path_iD in ret_path_iDs:
					#node_pathL_dict[node].remove(path_iD)
					pass
				else:		
					path_iD_node_load[path_iD] += 1
					overlapping_paths.add(path_iD)

		for edge in gc.get_all_edges_from_SOP([maxP]):
			for path_iD in edge_pathL_dict[edge]:
				path_iD_edge_load[path_iD] += 1
				if edge in newly_covered_edges:
					path_iD_edge_coverage[path_iD] -= 1
				if path_iD in ret_path_iDs:
					pass
				else:

					overlapping_paths.add(path_iD)
		
		# update their scores (heap.update(path_iD,new_score))
		for path_iD in overlapping_paths:
			path = path_dict[path_iD]
			edge_C_score = path_iD_edge_coverage[path_iD]
			edge_L_score = path_iD_edge_load[path_iD]
			node_L_score = path_iD_node_load[path_iD]
			if path_iD_MS_score.get(path_iD, None) == None:
				path_iD_MS_score[path_iD] = cos.score_MS(path, used_MS_set)
			MS_score = path_iD_MS_score[path_iD]
			score  = ((COVERAGE * edge_C_score) + (EDGE_LOAD * edge_L_score) + 
					(NODE_LOAD * node_L_score)) + MS*MS_score
			heap.update(path_iD, score)
	return ret_path_iDs

def func_wrapper_greedy_algo(t_path_dict, t_uncovered_edges, coeffs, s_coeff):
	'''
	- Input:
	Given a dictionary of path IDs, set of uncovered edges, a set of coefficients, a new coefficent,
	calls the greedy algorithm those inputs

	- Output:
	Returns the tuples of metrics on the set of probing paths the greedy algorithm picked
	'''
	node_loads = {}
	edge_loads = {}
	coeffs[1] = s_coeff
	ret_paths = greedy_algorithm(t_path_dict, t_uncovered_edges, node_loads, edge_loads, coeffs)
	num_paths_picked = len(ret_paths)
	monitoring_nodes = set()
	
	for path_iD in ret_paths:
		monitoring_nodes.add(t_path_dict[path_iD][0])
		monitoring_nodes.add(t_path_dict[path_iD][-1])
	num_MS = len(monitoring_nodes)

	total_node_load = 0
	max_node_load = 0
	max_node_load_iD = 0

	for nd in node_loads:
		node_load = node_loads[nd]
		total_node_load += node_load
		if node_load > max_node_load:
			max_node_load = node_load
			max_node_load_iD = nd
	avg_node_load = float(total_node_load)/len(node_loads)

	total_edge_load = 0
	max_edge_load = 0
	max_edge_load_iD= 0

	for eg in edge_loads:
		edge_load = edge_loads[eg]
		total_edge_load += edge_load

		if edge_load > max_edge_load:
			max_edge_load = edge_load
			max_edge_load_iD = eg

	avg_edge_load = float(total_edge_load)/len(edge_loads)
	return (num_paths_picked, num_MS, avg_node_load, max_node_load, 
		avg_edge_load, max_edge_load)