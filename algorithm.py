import matplotlib.pyplot as plt
import networkx as nx 
import random

G = nx.fast_gnp_random_graph(10,0.8,1,False)

H = G.copy()

labelsdict = {}

for node in H.nodes():
	labelsdict[node] = str(node)

pos=nx.spring_layout(H)

nx.draw(H, labels = labelsdict, with_label = True)

#nx.draw(H)
plt.show()


for (u,v) in H.edges():
	H[u][v]['w'] = random.randint(0,10)
	#H[u][v]['covered'] = False


set_of_paths_P = nx.all_pairs_shortest_path(H)


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

setP = removeDuplicate(set_of_paths_P) 
#print setP 

def get_all_edges_from_SOP(setP):
	retL = []
	for path in setP:
		for i in xrange(len(path)-1):
			temp = (path[i],path[i+1])
			tempRev = (path[i+1], path[i])
			if not (temp in retL or tempRev in retL):
				retL.append(temp)
	return retL

gEFS = get_all_edges_from_SOP(setP)

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

setPaths = greedyAlgorithm(setP, gEFS)
#print setPaths
print evaluateGreedyResult(setPaths)











