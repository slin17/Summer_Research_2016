import os
import sys
import csv
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm

def auto_scatter(divine_dict, four_tuples):
	plot_tuples, graph_iDs_range, plot_average, combine = four_tuples[0], four_tuples[1], four_tuples[2], \
															four_tuples[3]

	num_frac = len(divine_dict['0'])
	
	markers_L = [".",",","o","v","^","<",">","8"]
	label_dict = {0: 'Frac', 1: 'Num Paths', 2: 'Num Beacons', 3: 'Avg Node Load', \
				4: 'Max Node Load', 5: 'Avg Edge Load', 6: 'Max Edge Load'}
	l_plots = list() # l_plots stores the matplotlib plot objects
	if combine:
		# initializes plot objects
		i = 0
		while i < len(plot_tuples):
			plot = plt.subplots()
			l_plots.append(plot)
			i += 1	
	first_time = True
	for graph_iD in graph_iDs_range:
		colors = iter(cm.rainbow(np.linspace(0,1,num_frac+1)))
		

		if not combine:
			l_plots = list() # l_plots stores the matplotlib plot objects
			# initializes plot objects
			i = 0
			while i < len(plot_tuples):
				plot = plt.subplots()
				l_plots.append(plot)
				i += 1

		m_i = 0
		frac_dicts = divine_dict[str(graph_iD)]
		frac_list = frac_dicts.keys()
		frac_list.sort()
		for frac in frac_list:
			col = next(colors)
			mark = markers_L[m_i%len(markers_L)]
			frac_data = frac_dicts[frac]
			num_iter = len(frac_data[0])
			for k in xrange(len(l_plots)):
				x_p,y_p = plot_tuples[k]
				ax = l_plots[k][1]
				if plot_average:
					x_res = sum(frac_data[x_p-1])/float(num_iter) if x_p != 0 else float(frac)
					y_res = sum(frac_data[y_p-1])/float(num_iter) if y_p != 0 else float(frac)
					ax.scatter([x_res], [y_res], c = col, s = 70, marker = mark, label = frac)
				else:
					x_res = frac_data[x_p-1] if x_p != 0 else [float(frac)]*num_iter
					y_res = frac_data[y_p-1] if y_p != 0 else [float(frac)]*num_iter
					ax.scatter(x_res, y_res, c = col, s = 70, marker = mark, label = frac)
				ax.set_xlabel(label_dict[x_p])
				ax.set_ylabel(label_dict[y_p])
				if first_time or not combine:
					if not (x_p == 0 or y_p == 0):
						ax.legend(loc = 'upper right')
			m_i += 1
		if not combine:
			for k in xrange(len(l_plots)):
				fig, ax = l_plots[k]
				fig.canvas.set_window_title("graph id: %d" %(graph_iD))
			plt.show()
		first_time = False
	if combine:
		for k in xrange(len(l_plots)):
			fig, ax = l_plots[k]
			fig.canvas.set_window_title('Combined Plot')
			# ax.set_title(graph_iD)
		plt.show()

def parse_input_str(s, default_end):
	'''
	s is in the form:
	1,2;5,0:1-6,8,-5,10-:T:F

	1,2;5,0 > plots columns 1 vs 2 and 5 vs 0 from source csv file
	1-6,8,-5,10- > graph id ranges (1 to 6), 8, (0 to 5), (10 - end)
	T > plot average True
	F > combine False
	'''
	str_L = s.split(':')
	plot_L = str_L[0].split(';')
	plot_tuples = list()
	for plot_s in plot_L:
		two_L = plot_s.split(',')
		plot_tuples.append((int(two_L[0]),int(two_L[1])))
	graph_iD_ranges = parse_str_n_produce_range(str_L[1], default_end)
	if len(str_L) <= 2:
		bool1, bool2 = False, False
	elif len(str_L) <= 3:
		bool1, bool2 = (str_L[2][0] in 'tT'), False
	else:
		bool1, bool2 = (str_L[2][0] in 'tT'), (str_L[3][0] in 'tT')
	return (plot_tuples, graph_iD_ranges, bool1, bool2)

def parse_str_n_produce_range(s, default_end):
	ret_L, n, j = list(), None, 0
	for i in xrange(len(s)):
		if s[i] == '-':
			n = int(s[j:i]) if j < i else 0
			j = i + 1
			if i == len(s) -1:
				ret_L += range(n, default_end+1)
		elif s[i] == ',' or i == len(s) -1:
			if i == len(s) -1:
				new_n = int(s[j:])
			else:
				new_n = int(s[j:i]) if j < i else default_end
			if n == None:
				ret_L += [new_n]
			else:
				to_append = range(n, new_n+1)
				ret_L += to_append
			j = i+1
			n = None
	return ret_L

def read_from_csv(source_file):
	rows = csv.reader(open(os.path.expanduser('./data/csv/'+ source_file +'.csv')))
	ret_dict = dict()
	graph_iD, prev_frac = None, None 
	new_graph, new_frac = True, True

	# 0 - num_paths, 1 - num_beacons, 2 - avg_node_load, 3 - max_node_load, 4 - avg_edge_load, 
	# 5 - max_edge_load
	result = [[] for x in range(6)]
	frac_dict = dict()
	for row in rows:
		if len(row[0]) < 1 or row[0] == 'Graph Params: ' or row[0] == 'New Graph':
			continue 
		if graph_iD == None:
			graph_iD = row[0]
			new_graph = False
		else:
			if graph_iD != row[0]:
				new_graph = True
		if prev_frac == None:
			prev_frac = float(row[1])
		else:
			if prev_frac != float(row[1]):
				frac_dict[prev_frac] = result
				result = [[] for x in range(6)]
				prev_frac = float(row[1])

		if new_graph:
			ret_dict[graph_iD] = frac_dict
			frac_dict = dict()
			graph_iD = row[0]
			new_graph = False

		for j in xrange(6):
			if j == 0:
				offset = 2
			else:
				offset = 3
			result[j].append(float(row[j+offset]))
	frac_dict[prev_frac] = result
	ret_dict[graph_iD] = frac_dict
	return ret_dict

def main(source_file):
	divine_dict = read_from_csv(source_file)
	while True:
		try:
			line = raw_input()
			s = line.strip('\n')
			ftup = parse_input_str(s, len(divine_dict))
			auto_scatter(divine_dict, ftup)
		except EOFError:
			break

if __name__ == '__main__':
	main(sys.argv[1])