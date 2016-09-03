"""
compu_score.py
A module for calculating and updating scores for various network metrics
"""

import graph_cleanup as gc
import random
import sys


def random_tie_breaker(path_iD_set, path_iD_MS_score, frac, \
				path_iD_edge_load, path_iD_edge_coverage):
	"""
	Given list of paths with the same score, breaks the tie using either edge 
	coverage or edge load depending on the fraction
	"""
	if len(path_iD_set) == 1:
		return path_iD_set.pop(), 1

	rsd = dict()
	m_score = sys.maxint if frac <= 0.5 else 0
	for path in path_iD_set:
		if frac > 0.5:
			score = path_iD_edge_coverage[path]
		elif frac <= 0.5:
			score = path_iD_edge_load[path]
		else:
			score = path_iD_MS_score.get(path, 0)
		rsd.setdefault(score, set()).add(path)
		if frac <= 0.5:
			m_score = min(m_score, score)
		else:
			m_score = max(m_score, score)

	ret_size = len(rsd[m_score])
	ret_idx = random.sample(rsd[m_score], 1)

	return ret_idx[0], ret_size


def rand_tie_breaker(path_iD_set):
	"""
	Given a list of path IDs, returns a random path ID from that list
	"""
	if len(path_iD_set) == 1:
		return path_iD_set.pop(), 1
	else:
		ret_idx = random.sample(path_iD_set,1)
		return ret_idx[0], 1

		
def score_edge_coverage(path, uncoveredS):
	"""
	Given a path and a set of uncovered edges, returns a score representing the number
	of uncovered edges that the path goes through
	"""
	retScore = 0
	for i in xrange(len(path)-1):
		temp = gc.edge_id((path[i],path[i+1]))
		if  temp in uncoveredS:
			retScore += 1
	return retScore


def score_MS(path, used_MS_set):
	"""
	Given a path and a set of used monitoring stations, returns an score representing the number of
	beacons the path reuses
	"""
	if path[0] in used_MS_set and path[-1] in used_MS_set:
		return 2
	elif path[0] in used_MS_set or path[-1] in used_MS_set:
		return 1
	else:
		return 0


def node_load_score(path, node_loads):
	"""
	Given a path and a dictionary mapping nodes to their loads, returns a score representing
	the total load on the paths's nodes
	"""
	score = 0
	for nd in path:
		score += node_loads.get(nd, 0)
	return score


def edge_load_score(path, edge_loads):
	"""
	Given a path and a dictionary mapping edges to their loads, returns a score representing
	the total load on the paths's edges
	"""
	score = 0
	for i in xrange (len(path) - 1):
		edge = gc.edge_id((path[i], path[i + 1]))
		score += edge_loads.get(edge, 0)
	return score


def update_load_values(path, node_loads,edge_loads):
	"""
	Given a probing path, updates the node load and edge load dictionaries for each
	node and edge along the path
	"""
	#update node loads
	for nd in path:
		node_loads[nd] = node_loads.get(nd, 0) + 1

	#update edge loads
	for i in range(len(path) - 1):
		edge = gc.edge_id((path[i], path[i + 1]))
		edge_loads[edge] = edge_loads.get(edge, 0) + 1
