import sys
import matplotlib.pyplot as plt
import networkx as nx 
import random

#Global Variables
node_loads = {}
edge_loads = {}
paths_used = {}


def draw_graph(H):
	labelsdict = {}
	for node in H.nodes():
		labelsdict[node] = str(node)
	pos=nx.spring_layout(H)
	nx.draw(H, labels = labelsdict, with_label = True)
	plt.show()


def removeDuplicate(set_of_paths_P):
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
	retL = []
	for path in setP:
		for i in xrange(len(path)-1):
			temp = (path[i],path[i+1])
			tempRev = (path[i+1], path[i])
			if not (temp in retL or tempRev in retL):
				retL.append(temp)
	return retL


def scoreFunc(path, uncoveredL):
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


def greedyAlgorithm(setP, uncoveredL):

	#coeficients
	EDGE_COVERAGE = 1
	EDGE_LOAD = 0
	NODE_LOAD = 0
	
	retPaths = []
	usedMSL = set()
	hSDict = {}
	maxP = []
	while len(uncoveredL) > 0:
		maxScore = -1
		
		for path in setP:
			score = scoreFunc(path, uncoveredL)
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
		setP.remove(maxP)		#remove shoden path from the chosen path

		#update load values
		update_load_values(maxP)
	return retPaths
	
	
def evaluateGreedyResult(setPaths):
	S = set()
	for path in setPaths:
		S.add(path[0])
		S.add(path[len(path)-1])
	return S


def generate_graphs_params(filename):
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
    #read graph creation properties from file
    g = generate_graphs_params(filename)
    G = nx.fast_gnp_random_graph(g[0], g[1], g[2], False)
    
    #add edge weights 
    H = G.copy()
    randSeed = g[5]
    for (u,v) in H.edges():
    	random.seed(randSeed)
    	rInt = random.randint(g[3],g[4])
    	H[u][v]['w'] = rInt
    	randSeed += 1

    draw_graph(H)

    set_of_paths_P = nx.all_pairs_shortest_path(H)
    setP = removeDuplicate(set_of_paths_P)
    uncovered_edges = get_all_edges_from_SOP(setP)

    #initialize all network loads to 1
    nds = G.nodes();
    for nd in nds:
        node_loads[nd] = 1
        
    for e in uncovered_edges:
        edge_loads[e] = 1

    retPaths = greedyAlgorithm(setP, uncovered_edges)
    #print retPaths
    print "the size of retPaths: ", len(retPaths)
    print_result(retPaths, setP)


#*********************************************
def node_load_score(path):
    score = 0
    for nd in path:
        score += node_loads[nd]
        
    return score


def edge_load_score(path):
    score = 0
    for i in range (len(path) - 1):
        edge = (path[i], path[i + 1])
        rev_edge = (path[i + 1], path[i])
        
        if edge in edge_loads:
            score += edge_loads[edge]
        elif rev_edge in edge_loads:
            score += edge_loads[rev_edge]
    
    return score


def update_load_values(path):
    #update node loads
    for nd in path:
        node_loads[nd] += 1;
        
    #update edge loads
    for i in range(len(path) - 1):
        edge = (path[i], path[i + 1])
        rev_edge = (path[i + 1], path[i])
        
        if edge in edge_loads:
            edge_loads[edge] += 1
        elif rev_edge in edge_loads:
            edge_loads[rev_edge] += 1


def print_result(retpaths, inpaths):
	file = open("results.txt", 'a')

	file.write("\nPaths Used During Probing: \n")
	file.write(str(retpaths))


	file.write("\n\nNodes Used as Monitoring Stations: \n")
	file.write(str(nodes_used) + "\n")	#we need to change the data structure

	#calculate node load results
	total_load = 0
	max_load = 0
	max_load_at = 0

	for nd in node_loads:
		load = node_loads[nd]
		total_load += load

		if load > max_load:
			max_load = load
			max_load_at = nd

	mean_load = total_load/len(node_loads.keys())

	file.write("\n********************************\nNode Loads\n" +
		"- Average Node Load: " + str(mean_load) +
		"\n- Maximum Node Load: " + str(max_load) + " on node " + str(max_load_at))
	file.write("\n All Node Loads: \n" + str(node_loads))

	#calculate edge load results
	total_load = 0
	max_load = 0
	max_load_at = 0

	for eg in edge_loads:
		load = edge_loads[eg]
		total_load += edge_loads[eg]

		if load > max_load:
			max_load = load
			max_load_at = eg

	mean_load = total_load / len(edge_loads.keys())

	file.write("\n\n********************************\nEdge Loads\n" +
		"- Average Edge Load: " + str(mean_load) +
		"\n- Maximum Edge Load: " + str(max_load) + " on edge " + str(max_load_at))
	file.write("\n All Edge Loads: \n" + str(edge_loads))

	file.close()


if __name__ == "__main__":
    main(sys.argv[1])












