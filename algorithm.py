import sys
import matplotlib.pyplot as plt
import networkx as nx 
import random

#G = nx.fast_gnp_random_graph(15,0.5,5,False)

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
    params_graph = []  # a list of graph creation arguments
    
    #get graph creation parameters
    try:
        #file = open(filename, "r")
		file = open("test_graphs_params.txt", "r")
		line = file.readline()
		
		while line != "":
			values = line.strip().split("\t")
			values[0] = int(values[0])
			values[1] = float(values[1])
			values[2] = int(values[2])
			values[3] = int(values[3]) #the start point for randint func
			values[4] = int(values[4]) #the end point for randint func
			values[5] = int(values[5]) #the seed for randint 
			params_graph.append(values)
			line = file.readline()
			return params_graph
            
    except FileNotFoundError as e:
        raise ("Cannot open file: " + str(e))
   
    
def main(filename):
    
    #read graph creation properties from file
    
    test_graphs = generate_graphs_params(filename)
    
    #graph to be used for testing
    g = test_graphs[0]
    G = nx.fast_gnp_random_graph(g[0], g[1], g[2], False)
    
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
    uncoveredL = get_all_edges_from_SOP(setP)
    retPaths = greedyAlgorithm(setP, uncoveredL)


if __name__ == "__main__":
    main(sys.argv[1])











