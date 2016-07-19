def edge_id(edge):
	if (edge[0] > edge[1]):
		return (edge[1], edge[0])
	else: return edge

def remove_duplicate_paths(set_of_paths_P):
	'''
	Given a set of paths, remove the duplicated ones 
	[1,2,3] and [3,2,1] are the same. So, one of them is a duplicate
	Input:
		a set of paths (a list of lists)
	Output:
		a set of paths with duplicates removed
	'''
	retListofL = []
	set_of_end_points = set()
	for start_node in set_of_paths_P.keys():
		for end_node in set_of_paths_P[start_node].keys():
			pathL = set_of_paths_P[start_node][end_node]
			if len(pathL) > 1:
				# copy_path = pathL[:]
				# copy_path.reverse()
				#if not (pathL in retListofL or copy_path in retListofL):
				if edge_id((start_node,end_node)) not in set_of_end_points:
					retListofL.append(pathL)
					set_of_end_points.add(edge_id(start_node,end_node))
	return retListofL

def get_all_edges_from_SOP(setP):
	'''
	Given a path (list of edges/tuples), get all the edges without duplicates 
	(1,2) and (2,1) are the same. So, one of them is a duplicate
	Input:
		a path (list of edges/tuples)
	Output:
		set of edges/tuples
	'''
	ret_set = set()
	for path in setP:
		for i in xrange(len(path)-1):
			temp = edge_id((path[i],path[i+1]))
			ret_set.add(temp)
	return ret_set

def delete_edges_from_s(path, uncoveredS):
	'''
	Given a path (set of edges/tuples) and a list of uncovered edges
	if a given path has an "uncovered" edge, delete the edge in the list of uncovered edges
	Input:
		a path (set of edges/tuples) and a list of uncovered edges
	Output:
		None 
	'''
	ret_set_edges = set()
	for i in xrange(len(path)-1):
		temp = edge_id((path[i],path[i+1]))
		if temp in uncoveredS:
			uncoveredS.remove(temp)
			ret_set_edges.add(temp)
	return ret_set_edges