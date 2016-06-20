def testFunc():
	file = open("test_graphs_params.txt", "r")
	listofLines = file.readlines()
	print listofLines
	file.close()

testFunc()