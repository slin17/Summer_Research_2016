import csv

def iterate_func(num_iterations, indx, list_of_uncovered_edges, info_dict, coeff, func, *args):
	idx = 0
	while idx < num_iterations:
		s_uncovered_edges = set(list_of_uncovered_edges[indx])
		six_tuple = func(args[0], s_uncovered_edges, args[1], coeff)
		for i in xrange(6):
			info_dict[i].append(six_tuple[i])
		idx += 1
	return max(info_dict[5])


# b_s_1 - binary search for end point for a range, in which max of the metric
# we care about is optimum
def b_s_1(coeff, num_iter, indx, list_of_uncovered_edges, func, *args):
	start_coeff = None
	max_Max_edge_load = None
	pow_two = 0
	file = open("re_bsC1d.csv", 'at')
	writer = csv.writer(file)
	while max_Max_edge_load == None or max_Max_edge_load > 1:
		start_coeff = coeff
		coeff += (-0.25*pow_two)
		writer.writerow(("current coefficient: ", coeff))
		info_dict = dict()
		#initialize info_dict
		for i in xrange(6):
			info_dict[i] = []
		idx = 0
		max_Max_edge_load = iterate_func(num_iter, indx, list_of_uncovered_edges, info_dict, coeff, func, *args)
		#increment powers of 2
		if pow_two == 0:
			pow_two = 1
		else:
			pow_two = pow_two << 1
	file.close()
	return (start_coeff, coeff)

def b_s_2(start_coeff, end_coeff, num_iter, indx, list_of_uncovered_edges, func, *args):
	'''
	We always know that low is the correct one because we move set low = mid_coeff
	Only if mid_coeff gives us max_Max_edge_load of 1
	'''
	opt_coeff = None
	high = start_coeff
	low = end_coeff
	limit = 0
	file = open("re_bsC2d.csv", 'at')
	writer = csv.writer(file)
	while low < high and limit < 5:
		mid_coeff = (low + high)/2
		writer.writerow(("current mid_coefficient: ", mid_coeff))
		max_Max_edge_load = None
		info_dict = dict()
		for i in xrange(6):
			info_dict[i] = []
		max_Max_edge_load = iterate_func(num_iter, indx, list_of_uncovered_edges, info_dict, mid_coeff, func, *args)
		if max_Max_edge_load == 1:
			low = mid_coeff
		else:
			high = mid_coeff
		limit += 1
	opt_coeff = min(low, high)
	file.close()
	return opt_coeff

