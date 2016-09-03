"""
graph_cleanup.py
A module for reading and configuring the input to the probing algorithm
"""

def edge_id(edge):
	'''
	Given an edge, returns a version of the edge where the lower node
	number is always first
	'''
	if (edge[0] > edge[1]):
		return (edge[1], edge[0])
	else: return edge


def remove_duplicate_paths(set_of_paths_P, num_nodes):
	'''
	Given a set of paths, return a list of all the unique paths. [1,2,3] and [3,2,1]
	are considered the same, only one will appear in the output list
	'''
	retListofL = []
	for i in xrange(num_nodes):
		for j in xrange(i):
			if j in set_of_paths_P[i]:
				ori_path = set_of_paths_P[i][j]
				retListofL.append(ori_path)
				copy_path = set_of_paths_P[j][i][:]
				copy_path.reverse()
				if ori_path != copy_path:
					retListofL.append(set_of_paths_P[j][i])
	return retListofL


def get_all_edges_from_SOP(setP):
	'''
	Given a list of paths, returns a set of all the edges found in the set
	of paths
	'''
	ret_set = set()
	for path in setP:
		for i in xrange(len(path)-1):
			temp = edge_id((path[i],path[i+1]))
			ret_set.add(temp)
	return ret_set


def delete_edges_from_s(path, uncoveredS):
	'''
	Given a path and a list of uncovered edges, deletes from the list
	all edges in the path 
	'''
	ret_set_edges = set()
	for i in xrange(len(path)-1):
		temp = edge_id((path[i],path[i+1]))
		if temp in uncoveredS:
			uncoveredS.remove(temp)
			ret_set_edges.add(temp)
	return ret_set_edges