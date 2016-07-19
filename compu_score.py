import graph_cleanup as gc
import random

def random_tie_breaker(path_iD_list):
	if len(path_iD_list) == 0:
		return path_iD_list[0]
	else:
		ret_idx = random.randint(0, len(path_iD_list)-1)
		return path_iD_list[ret_idx]

def score_edge_coverage(path, uncoveredS):
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
		temp = gc.edge_id((path[i],path[i+1]))
		if  temp in uncoveredS:
			retScore += 1
	return retScore

def score_MS(path, used_MS_set):
	if path[0] in used_MS_set and path[-1] in used_MS_set:
		return 2
	elif path[0] in used_MS_set or path[-1] in used_MS_set:
		return 1
	else:
		return 0

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
		score += edge_loads.get(edge, 0)
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
		edge = gc.edge_id((path[i], path[i + 1]))
		edge_loads[edge] = edge_loads.get(edge, 0) + 1
