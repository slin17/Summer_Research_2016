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
				if path not in hSDict[score]:
					hSDict[score].append(path)

		lP = hSDict[hSDict.keys()[0]]
		if len(lP) > 1:
			
			maxP = tieBreakerPath(lP, usedMSL)
			
		else:
			maxP = lP[0]

		deleteEdgesFromL(maxP, uncoveredL)
		retPaths.append(maxP)
		usedMSL.add(maxP[0])
		usedMSL.add(maxP[-1])
		setP.remove(maxP)
	print "usedMSL: ", usedMSL
	print "size of usedMSL: ", len(usedMSL)
	return retPaths

'''
testPaths = [[1,2,3],[1,2,5,3],[1,4,3],[1,4,5,3],[2,5],[4,5],[4,3],[2,3],[3,4]]
testUncoverdL = [(1,2),(1,4),(2,5),(5,4),(2,3),(5,3),(4,3)]
print greedyAlgorithm(testPaths, testUncoverdL)
'''


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
    print retPaths
    print "the size of retPaths: ", len(retPaths)


if __name__ == "__main__":
    main(sys.argv[1])












