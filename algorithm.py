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


def greedyAlgorithm(setP, uncoveredL):
	#coeficients
    EDGE_COVERAGE = 1
    EDGE_LOAD = 0
    NODE_LOAD = 0

	retPaths = []
	while len(uncoveredL) > 0:
		maxScore = 0
		maxP = []
		for path in setP:
			score = scoreFunc(path, uncoveredL)
			if score > maxScore:
				maxP = path
		deleteEdgesFromL(maxP, uncoveredL)
		retPaths.append(maxP)
	return retPaths


def evaluateGreedyResult(setPaths):
	S = set()
	for path in setPaths:
		S.add(path[0])
		S.add(path[len(path)-1])
	return S


def generate_graphs_params(filename):
	param_graphs = []
	file = open(filename, "r")
	line = file.readline().strip().split()
	for i in xrange(len(line)):
		if i == 1:
			param_graphs.append(float(line[i]))
		else:
			param_graphs.append(int(line[i]))

	return param_graphs


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

    #initialize all network loads to 1
    nds = G.nodes();
    for nd in nds:
        node_loads[nd] = 1
        
    for e in uncovered_edges:
        edge_loads[e] = 1

    draw_graph(H)

    set_of_paths_P = nx.all_pairs_shortest_path(H)
    setP = removeDuplicate(set_of_paths_P)
    uncoveredL = get_all_edges_from_SOP(setP)
    retPaths = greedyAlgorithm(setP, uncoveredL)
    print retPaths


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


if __name__ == "__main__":
    main(sys.argv[1])











