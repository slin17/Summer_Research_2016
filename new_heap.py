import sys
'''
Saw S. Lin 

Max heap, using array
If parent is at index p, then its left child is at 2*p and 
right at 2*p +1

_score_pos dict: stores score as key and position in the array as value

_score_path_id: stores score as key and set of path ids as value

_path_id_score: path id as key and score as value (for easy look up of old score, 
if update is called with new score)
'''
class New_Heap(object):
	def __init__(self):
		self._heap_list = [sys.float_info.max]
		self._score_pos = dict()
		self._score_path_id = dict()
		self._path_id_score = dict()

	def __len__(self):
		return len(self._heap_list)-1

	def __perc_up(self, i):
		while (i >> 1) > 0:
			par_i = i >> 1
			if self._heap_list[i] <= self._heap_list[par_i]:
				break

			curr_score = self._heap_list[i]
			par_score = self._heap_list[par_i]
			self._heap_list[par_i], self._heap_list[i] = \
				self._heap_list[i], self._heap_list[par_i]

			self._score_pos[curr_score] = par_i
			self._score_pos[par_score] = i
			i = par_i

	def __insert(self, k):
		self._heap_list.append(k)
		self._score_pos[k] = len(self)
		self.__perc_up(len(self))

	def add(self, path_id, k):
		self._score_path_id.setdefault(k,set()).add(path_id)
		self._path_id_score[path_id] = k
		if k not in self._score_pos:
			self.__insert(k)

	def __per_down(self, i):
		while (i << 1) <= len(self):
			max_c = self.__max_child(i)
			if self._heap_list[i] >= self._heap_list[max_c]:
				break
			curr_score = self._heap_list[i]
			child_score = self._heap_list[max_c]
			self._score_pos[curr_score] = max_c
			self._score_pos[child_score] = i
			tmp = self._heap_list[i]
			self._heap_list[i] = self._heap_list[max_c]
			self._heap_list[max_c] = tmp
			i = max_c

	def __max_child(self,i):
		left = i << 1
		if left+1 > len(self):
			return left
		else:
			if self._heap_list[left] > self._heap_list[left+1]:
				return left
			else:
				return left+1

	def update(self, path_id, k):
		if self._path_id_score[path_id] != k:
			self.remove(path_id)
			self.add(path_id, k)

	def remove(self, path_id):
		score = self._path_id_score.pop(path_id)
		scoreset = self._score_path_id[score]

		if len(scoreset) > 1:
			scoreset.remove(path_id)
		else:
			del self._score_path_id[score]
			pos = self._score_pos.pop(score)
			self._heap_list[pos] = self._heap_list.pop()
			self._score_pos[self._heap_list[pos]] = pos

			if pos > 1 and self._heap_list[pos] > self._heap_list[pos >> 1]:
				self.__perc_up(pos)
			else:
				self.__per_down(pos)
		
	def peek_all(self):
		if len(self) < 1:
			raise IndexError('Empty Heap')
		return set(self._score_path_id[self._heap_list[1]])

	def peek(self):
		return self._heap_list[1]